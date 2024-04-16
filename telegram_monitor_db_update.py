import os
import asyncio
import logging
from telethon import TelegramClient, events
import requests  # For sending POST requests to Slack webhook
import boto3
from datetime import datetime

# --- Configuration Section ---

# Telegram configuration
api_key = 'YOUR_TELEGRAM_API_KEY'  # Replace with your Telegram API key
api_hash = 'YOUR_TELEGRAM_API_HASH'  # Replace with your Telegram API hash
channels = ['CHANNEL_1', 'CHANNEL_2']  # Replace with your channel names or IDs

# Slack configuration
slack_webhook = "YOUR_SLACK_WEBHOOK_URL"  # Replace with your Slack webhook URL

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a Telegram client instance
client = TelegramClient('anon', api_key, api_hash)


# --- Functions Section ---

# Function to update a timestamp in a DynamoDB table
def update_timestamp(table_name, primary_key_name, primary_key_value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    current_timestamp = datetime.utcnow().isoformat()
    response = table.update_item(
        Key={
            primary_key_name: primary_key_value
        },
        UpdateExpression='SET last_updated_timestamp = :timestamp',
        ExpressionAttributeValues={
            ':timestamp': current_timestamp
        }
    )
    logger.info(f"Timestamp updated in DynamoDB: {response}")


# Asynchronous function to periodically update DynamoDB
async def update_dynamo_periodically():
    while True:
        table_name = 'easm_heartbeats'
        primary_key_name = 'service_name'
        primary_key_value = 'telegram_script'
        update_timestamp(table_name, primary_key_name, primary_key_value)
        await asyncio.sleep(1800)  # Sleep for 30 minutes


# Asynchronous function to send a message to Slack using a webhook
async def send_slack_message(text):
    payload = {"text": text}
    try:
        response = requests.post(slack_webhook, json=payload)
        response.raise_for_status()
        logger.info(f"Message sent successfully to Slack")
    except requests.RequestException as e:
        logger.error(f"Error sending message to Slack: {e}")


# Main asynchronous function
async def main():
    # Start periodic DynamoDB updates
    asyncio.create_task(update_dynamo_periodically())

    try:
        await client.start()
        # Fetch the Telegram channel entities based on channel names/IDs
        channel_entities = await asyncio.gather(*(client.get_entity(c) for c in channels))
    except Exception as e:
        logger.error(f"Error fetching channel information: {e}")
        return

    # Event handler for new messages in the specified Telegram channels
    @client.on(events.NewMessage(chats=channel_entities))
    async def my_event_handler(event):
        try:
            sender = await event.get_sender()
            channel = await event.get_chat()
            message = event.raw_text

            text = f"Telegram Alert\nChannel: {(channel.title)}\nUser: {sender.username}\nMessage: {message}\n"
            logger.info(f"Message received from {sender.username} in {channel.title}: {message}")

            # Send the message to Slack
            await send_slack_message(text)

        except Exception as e:
            logger.error(f"Error processing message: {e}")

    # Run the Telegram client until it gets disconnected
    try:
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"Error running Telegram client: {e}")


# Execute the main asynchronous function
asyncio.run(main())

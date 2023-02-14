import json
import requests
from typing import Union


# Should be treated like an environment variable and secret.
API_KEY = "YOUR_API_KEY"


class IPQS(object):
    """
    Class for interacting with the IPQualityScore API.

    Attributes:
        key (str): Your IPQS API key.
        format (str): The format of the response. Default is 'json', but you can also use 'xml'.
        base_url (str): The base URL for the IPQS API.

    Methods:
        email_validation_api(email: str, timeout: int = 1, fast: str = 'false', abuse_strictness: int = 0) -> str:
            Returns the response from the IPQS Email Validation API.
    """

    key = None
    format = None
    base_url = None

    def __init__(self, key, format="json") -> None:
        self.key = key
        self.format = format
        self.base_url = f"https://www.ipqualityscore.com/api/{self.format}/"

    def email_validation_api(self, email: str, timeout: int = 7, fast: str = 'false', abuse_strictness: int = 0) -> str:
        """
        Returns the response from the IPQS Email Validation API.

        Args:
            email (str):
                The email you wish to validate.
            timeout (int):
                Set the maximum number of seconds to wait for a reply from an email service provider.
                If speed is not a concern or you want higher accuracy we recommend setting this in the 20 - 40 second range in some cases.
                Any results which experience a connection timeout will return the "timed_out" variable as true. Default value is 7 seconds.
            fast (str):
                If speed is your major concern set this to true, but results will be less accurate.
            abuse_strictness (int):
                Adjusts abusive email patterns and detection rates higher levels may cause false-positives (0 - 2).

        Returns:
            str: The response from the IPQS Email Validation API.
        """

        url = f"{self.base_url}email/{self.key}/{email}"

        params = {
            "timeout": timeout,
            "fast": fast,
            "abuse_strictness": abuse_strictness
        }

        response = requests.get(url, params=params)
        return response.text

    def phone_number_validation_api(self, phone_number: str, country: Union[str, list], strictness: int = 0) -> str:
        """
        Returns the response from the IPQS Phone Number Validation API.

        Args:
            phone_number (str):
                The phone number you wish to validate.
            country (str or list):
                You can optionally provide us with the default country or countries this phone number is suspected to be associated with.
                Our system will prefer to use a country on this list for verification or will require a country to be specified in the event the phone number is less than 10 digits.
            strictness (int):
                Adjusts the strictness of the phone number validation. Higher levels may cause false-positives (0 - 2)

        Returns:
            str: The response from the IPQS Phone Number Validation API.
        """

        url = f"{self.base_url}phone/{self.key}/{phone_number}"

        params = {
            "country": country,
            "strictness": strictness
        }

        response = requests.get(url, params=params)
        return response.text


if __name__ == "__main__":

    email = 'taget_email@example.com'
    phone_number = '12025551212'

    ipqs = IPQS(API_KEY)
    print(ipqs.base_url)

    print(ipqs.email_validation_api(email))
    print(ipqs.phone_number_validation_api(phone_number, 'US'))


from censys.search import CensysHosts

# Open the file with the IP addresses
with open('ip_addresses.txt', 'r') as f:
    ip_addresses = [line.strip() for line in f]

# Create a CensysHosts instance
h = CensysHosts()

# Loop over each IP address and fetch its information
for ip_address in ip_addresses:
    # Fetch the host and its services
    host = h.view(ip_address)

    # Extract and print the relevant information
    print(f"IP Address: {host['ip']}")
    print(f"Organization: {host.get('autonomous_system', {}).get('name', 'N/A')}")
    print(f"Location: {host.get('location', {}).get('country', 'N/A')}")
    print(f"Operating System: {host.get('metadata', {}).get('os', 'N/A')}")

    # Check if port 443 is open for HTTP or HTTPS
    if '443/https' in host.get('protocols', []) or '443/http' in host.get('protocols', []):
        cert = host.get('443/https', {}).get('tls', {}).get('certificate', {})
        print(f"Certificate Information:")
        print(f"Subject: {cert.get('subject', {}).get('common_name', 'N/A')}")
        print(f"Issuer: {cert.get('issuer', {}).get('common_name', 'N/A')}")
        print(f"Validity Start Date: {cert.get('validity', {}).get('start', 'N/A')}")
        print(f"Validity End Date: {cert.get('validity', {}).get('end', 'N/A')}")
        print(f"Email Address: {cert.get('subject', {}).get('email_address', 'N/A')}")
        print(f"Organization: {cert.get('subject', {}).get('organization', 'N/A')}")
    elif '443/http' in host.get('protocols', []):
        print("Port 443 is open for HTTP but no certificate information is available")
    else:
        print("Port 443 is not open")

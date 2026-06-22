import requests

try:
    print("Attempting to ping Google API...")
    # We force a 5-second timeout so it doesn't hang forever
    response = requests.get("https://oauth2.googleapis.com/token", timeout=5)
    print(f"Connection Successful! (Status Code: {response.status_code})")
except Exception as e:
    print(f"Network Blocked! Error: {e}")
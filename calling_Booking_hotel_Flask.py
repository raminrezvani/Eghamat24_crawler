# Example 1: Using Python requests library
import requests

# Basic GET request with required parameters
url = "http://localhost:5040/booking_hotels"
params = {
    "start_date": "2025-04-20",
    "end_date": "2025-04-24",
    "adults": "2",
    "target": "KIH",
    "isAnalysis": "false",
    "hotelstarAnalysis": '[]',
    "priorityTimestamp": "1",
    "use_cache": "False"
}

response = requests.get(url, params=params)
if response.status_code == 200:
    print(response.json())
elif response.status_code == 204:
    print("Request processed successfully, no content returned")
else:
    print(f"Error: {response.status_code} - {response.json()['error']}")
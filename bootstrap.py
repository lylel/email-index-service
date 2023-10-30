import json
import requests

API_URL = "http://localhost:8000/v1/emails"

with open("emails.json", "r") as json_file:
    email_list = json.load(json_file)

for email_data in email_list:
    response = requests.post(API_URL, json=email_data)

    if response.status_code == 201:
        print(f"Email imported successfully: {email_data}")
    else:
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(f"Failed to import email: {email_data}")
        print(f"Response: {response.status_code} - {response.text}")

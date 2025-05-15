import os
import requests
import time

DISCORD_WEBHOOK_URL = os.getenv('https://discord.com/api/webhooks/1367789461093613580/v9mKlPyYhbmIAYHGraP7Wt4y2JwOTKFjYVIdyEshUDqmc1quVAOopeCqWUO4OCzsEkid')  # Set this in Vercel as an environment variable
API_URL = 'https://trex-beryl.vercel.app/api/scores'
CHECK_INTERVAL = 60  # Interval in seconds to check for changes

# Function to send a message to Discord
def send_to_discord(message):
    payload = {
        "content": message
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Discord: {e}")

# Function to check if the scores have changed
def check_for_changes(last_data):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        current_data = response.json()
        if current_data != last_data:
            print("Data changed, sending update to Discord...")
            send_to_discord(f"New scores update: {current_data}")
            return current_data  # Return new data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    return last_data

# This will be the entry point for Vercel
def handler(event, context):
    last_data = None
    while True:
        last_data = check_for_changes(last_data)
        time.sleep(CHECK_INTERVAL)

    return {
        "statusCode": 200,
        "body": "Watching for changes..."
    }

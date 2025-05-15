
import os
import requests
import time
import logging

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)

# Set environment variables for your Discord webhook URL
DISCORD_WEBHOOK_URL = os.getenv('https://discord.com/api/webhooks/1367789461093613580/v9mKlPyYhbmIAYHGraP7Wt4y2JwOTKFjYVIdyEshUDqmc1quVAOopeCqWUO4OCzsEkid')  # Ensure this is set in your Vercel environment variables
API_URL = 'https://trex-beryl.vercel.app/api/scores'
CHECK_INTERVAL = 10  # Check every 10 seconds, you can change this if needed

# Function to send a message to Discord
def send_to_discord(message):
    payload = {
        "content": message
    }
    try:
        # Send the message to the Discord webhook
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()  # This will raise an exception if the status code is 4xx/5xx
        logging.info("Message sent to Discord successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending message to Discord: {e}")

# Function to check for changes in the API data
def check_for_changes(last_data):
    try:
        logging.info("Fetching data from the API...")
        response = requests.get(API_URL)
        response.raise_for_status()  # Raises an exception for 4xx/5xx responses
        current_data = response.json()
        
        # Log the current data for debugging purposes
        logging.info(f"Current data from API: {current_data}")
        
        # If the data has changed, send an update to Discord
        if current_data != last_data:
            logging.info("Data has changed, sending update to Discord...")
            send_to_discord(f"New scores update: {current_data}")
            return current_data  # Return the updated data
        else:
            logging.info("No change in data.")
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
    
    return last_data

# Main function to handle the API polling
def handler(event, context):
    logging.info("Handler function started.")
    
    last_data = None  # Store the previous data to detect changes
    
    while True:
        last_data = check_for_changes(last_data)  # Check if the data has changed
        time.sleep(CHECK_INTERVAL)  # Wait before checking again

    return {
        "statusCode": 200,
        "body": "Watching for changes..."
    }

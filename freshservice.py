# freshservice.py
import os
import requests
import logging
import base64


def create_freshservice_ticket(ticket):
    url = f"https://{os.getenv('FRESHSERVICE_DOMAIN')}/api/v2/tickets"
    api_key = os.getenv('FRESHSERVICE_API_TOKEN')
    encoded_api_key = base64.b64encode(f"{api_key}:X".encode()).decode()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_api_key}"
    }
    data = {
        "description": ticket["body"],
        "subject": ticket["subject"],
        "email": ticket["sender"],
        "priority": 1,
        "status": 2,
        "group_id": int(os.getenv('FRESHSERVICE_GROUP_ID'))
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 201:
            logging.error(f"Failed to create ticket: {
                          response.status_code} - {response.text}")
        else:
            logging.info("Ticket created successfully")
    except Exception as e:
        logging.error(f"Error creating FreshService ticket: {e}")

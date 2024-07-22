# freshservice.py
import os
import requests
import logging
import base64


def create_freshservice_ticket(ticket):
    '''
    Accepts a dictionary with the following keys
    sender: str - email address of the sender (if account exists in FreshService, ticket will be associated with this user)
    subject: str - subject of the ticket (summary)
    body: str - body of the ticket (can be HTML)
    priority: int - priority of the ticket (1-4)
    status: int - status of the ticket (2 = open, 3 = pending, 4 = resolved, 5 = closed)
    group_id: int - ID of the group to assign the ticket to

    Creates a ticket in FreshService

    Returns None
    '''
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
            logging.error("Failed to create ticket: %s - %s",
                          response.status_code, response.text)
        else:
            logging.info("Ticket created successfully")
    except requests.ConnectionError:
        logging.error(
            "Network problem occurred while creating FreshService ticket")
    except requests.Timeout:
        logging.error("Timeout occurred while creating FreshService ticket")
    except requests.RequestException as e:
        logging.error("Error creating FreshService ticket: %s", e)

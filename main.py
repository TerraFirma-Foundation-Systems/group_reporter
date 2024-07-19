# main.py
import os
import time
import logging
import schedule
from freshservice import create_freshservice_ticket
from microsoft import get_users_not_in_group_sync
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_env():
    load_dotenv()


def run_task():
    logging.info("Running task...")
    group_id = os.getenv("GROUP_ID")
    filter_group_id = os.getenv("FILTER_GROUP_ID")
    if not group_id or not filter_group_id:
        logging.error(
            "GROUP_ID or FILTER_GROUP_ID environment variable not set")
        return

    try:
        users = get_users_not_in_group_sync(group_id, filter_group_id)
        if users:
            user_list = format_user_list(users)
            ticket = {
                "sender": "Alerts@goterrafirma.com",
                "subject": "Users not in SelfServicePasswordReset group",
                "body": user_list
            }
            create_freshservice_ticket(ticket)
        else:
            logging.info("No users found not in the group")
    except Exception as e:
        logging.error(f"Error running task: {e}")


def format_user_list(users):
    table = "<table><tr><th>Display Name</th><th>User Principal Name</th></tr>"
    for user in users:
        table += f"<tr><td>{user['displayName']
                            }</td><td>{user['userPrincipalName']}</td></tr>"
    table += "</table>"
    return table


def schedule_task(schedule_type):
    if schedule_type == "minute":
        schedule.every().minute.do(run_task)
    elif schedule_type == "hour":
        schedule.every().hour.do(run_task)
    elif schedule_type == "day":
        schedule.every().day.at("05:00").do(run_task)
    elif schedule_type == "monday":
        schedule.every().monday.at("05:00").do(run_task)
    elif schedule_type == "tuesday":
        schedule.every().tuesday.at("05:00").do(run_task)
    elif schedule_type == "wednesday":
        schedule.every().wednesday.at("05:00").do(run_task)
    elif schedule_type == "thursday":
        schedule.every().thursday.at("05:00").do(run_task)
    elif schedule_type == "friday":
        schedule.every().friday.at("05:00").do(run_task)
    elif schedule_type == "saturday":
        schedule.every().saturday.at("05:00").do(run_task)
    elif schedule_type == "sunday":
        schedule.every().sunday.at("05:00").do(run_task)
    else:
        logging.error(f"Invalid schedule type: {schedule_type}")


if __name__ == "__main__":
    load_env()
    run_schedule = os.getenv("RUN_SCHEDULE", "friday")
    logging.info(f"Scheduling task with schedule type: {run_schedule}")

    # Run the task immediately for testing
    run_task()

    # Schedule the task as usual
    schedule_task(run_schedule)

    while True:
        schedule.run_pending()
        time.sleep(60)

# microsoft.py
import os
import aiohttp
import asyncio
from msal import ConfidentialClientApplication
import logging


def get_msal_app():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    tenant_id = os.getenv("TENANT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    return ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)


def get_access_token():
    app = get_msal_app()
    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_for_client(scopes)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not acquire access token")


async def fetch_all_users(session, headers):
    users = []
    url = "https://graph.microsoft.com/v1.0/users"
    while url:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            result = await response.json()
            users.extend(result.get('value', []))
            url = result.get('@odata.nextLink')
    return users


async def fetch_user_membership(session, user, group_id, headers):
    url = f"https://graph.microsoft.com/v1.0/users/{user['id']}/memberOf"
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            memberships = await response.json()
            member_ids = [group['id']
                          for group in memberships.get('value', [])]
            if group_id in member_ids:
                return True
        return False


async def get_filtered_users(group_id, filter_group_id):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    async with aiohttp.ClientSession() as session:
        users = await fetch_all_users(session, headers)

        # Filter out users in the filter group
        filter_tasks = [fetch_user_membership(
            session, user, filter_group_id, headers) for user in users]
        filter_results = await asyncio.gather(*filter_tasks)
        filtered_users = [user for user, in_filter_group in zip(
            users, filter_results) if not in_filter_group]

        # Check remaining users' membership in the main group
        tasks = [fetch_user_membership(
            session, user, group_id, headers) for user in filtered_users]
        results = await asyncio.gather(*tasks)
        non_group_users = [user for user, in_group in zip(
            filtered_users, results) if not in_group]

        logging.info(f"Found {len(non_group_users)} users not in the group")
        return non_group_users


def get_users_not_in_group_sync(group_id, filter_group_id):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_filtered_users(group_id, filter_group_id))

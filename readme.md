# Group Reporter

SSO Reporter is a tool to monitor users in Microsoft Azure AD who are not in a specified group and create a ticket in FreshService with the list of these users. It is designed to run on a schedule and can be deployed using Docker.

## Features

- Fetches users from Microsoft Azure AD.
- Checks if users are not in a specified group.
- Excludes users from another specified filter group.
- Creates a ticket in FreshService with the list of users not in the specified group.
- Schedules the task to run at specified intervals.

## Requirements

- Python 3.8+
- Docker
- FreshService account
- Microsoft Azure AD account

## Setup

### Environment Variables

Create a `.env` file in the root directory based on the `env.example` file:

```plaintext
GROUP_ID=your_main_group_id
FILTER_GROUP_ID=your_filter_group_id
FRESHSERVICE_DOMAIN=your_freshservice_domain
FRESHSERVICE_API_TOKEN=your_freshservice_api_key
TENANT_ID=your_tenant_id
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
RUN_SCHEDULE=minute  # For testing, runs every minute
FRESHSERVICE_GROUP_ID=10000000701  # Replace with your actual group_id

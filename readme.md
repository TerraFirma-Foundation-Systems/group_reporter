# Group Reader

Group Reader is a tool to monitor users in Microsoft Azure AD who are not in a specified group and create a ticket in FreshService with the list of these users. It is designed to run on a schedule and can be deployed using Docker.

## Features

- Fetches users from Microsoft Azure AD.
- Checks if users are not in a specified group.
- Excludes users from another specified filter group.
- Creates a ticket in FreshService with the list of users not in the specified group.
- Schedules the task to run at specified intervals.

## Requirements

- Python 3.12+
- Docker
- FreshService account
- Microsoft Azure AD account

## Setup

### Environment Variables

Ensure the following environment variables are set in your Docker environment:

- `GROUP_ID`
- `FILTER_GROUP_ID`
- `FRESHSERVICE_DOMAIN`
- `FRESHSERVICE_API_TOKEN`
- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET`
- `RUN_SCHEDULE`
- `FRESHSERVICE_GROUP_ID`

### Installation

1. **Clone the Repository**

    ```bash
    git clone <your_repository_url>
    cd Group_Reader
    ```

2. **Set Up Virtual Environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

### Running Locally

To run the script locally:

```bash
python main.py
```

### Running with Docker

To run the script with Docker:

```bash
docker build -t group-reader .
docker run group-reader
```

or

```bash
docker-compose up --build
``` 

## Usage

The script will run once on launch (can be disabled) and then at the specified interval. It will fetch users from Microsoft Azure AD and check if they are not in the specified group. If they are not in the group, the script will create a ticket in FreshService with the list of users.

The schedule options are:

- minute
  - runs every mintue
- hour
  - runs every hour
- day
  - runs once daily at 5am
- monday
  - runs every Monday at 5am
- tuesday
  - runs every Tuesday at 5am
- wednesday
  - runs every Wednesday at 5am
- thursday
  - runs every Thursday at 5am
- friday
  - runs every Friday at 5am
- saturday
  - runs every Saturday at 5am
- sunday
  - runs every Sunday at 5am

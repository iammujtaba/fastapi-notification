# fastapi-notification
Notifications in FastAPI

## Installation

```bash
install redis on your local machine
install python version 3.11.x
```

Then create virtual environment and install the requirements
```bash
python3 -m venv venv
pip3 install -r requirements.txt
```

## Run

```bash
uvicorn fasnof.main:app --reload
```

These endpoints will fire an event to the respected user (1 and 2)
Even if the user is offline the event will be sent once the user is online
```bash

http://127.0.0.1:8000/notifications/profile/1
http://127.0.0.1:8000/notifications/profile/2
http://127.0.0.1:8000/notifications/subscription/1
http://127.0.0.1:8000/notifications/subscription/2
```

All the notifications will be visible here.
```
http://127.0.0.1:8000/?user_id=1
http://127.0.0.1:8000/?user_id=2
```

Current display format of the event
```
Event Name: SUBSCRIPTION_EXPIRY, Content: {'user_id': 2, 'title': 'Subscription Expiring Soon', 'description': 'Hurry up! Your subscription is expiring soon', 'event_name': 'SUBSCRIPTION_EXPIRY'}
```

Database will be created in the root directory with the name `fastnof.db`.

Use sqlite3 to view the database

Tech Used-
```
Python, FastAPI, Redis, Websockets, SQLAlchemy, SQLite
```

* Created a layer on top of sqlalchemy to make it easy to use and to make it more readable and feel like Django ORM.

* Used Redis as a message broker to send the events to the user.

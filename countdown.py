
# -*- coding: utf-8 -*-


import os
import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

# Competition start: January 3, 2028 at midnight
TZ = ZoneInfo("America/Toronto")
TARGET = datetime(2028, 1, 3, 0, 0, tzinfo=TZ)

def get_countdown():
    now = datetime.now(TZ)
    remaining = int((TARGET - now).total_seconds())

    sign = "-" if remaining < 0 else ""
    remaining = abs(remaining)

    days = remaining // 86400
    hours = (remaining % 86400) // 3600
    minutes = (remaining % 3600) // 60

    return (
        f"{sign}{days}j {hours}h {minutes}m "
        "avant Jeux de génie 2028"
    )

def update_slack_name(name):
    token = os.environ["SLACK_USER_TOKEN"]

    payload = json.dumps({
        "profile": {
            "real_name": name
        }
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://slack.com/api/users.profile.set",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read())

    if not result.get("ok"):
        raise RuntimeError(f"Slack API error: {result}")

    print(f"Updated Slack name: {name}")

if __name__ == "__main__":
    update_slack_name(get_countdown())

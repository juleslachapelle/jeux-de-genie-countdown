
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
        "avant les JDG 2028"
    )


def update_slack_name(name, token_name):
    token = os.environ[token_name]

    payload = json.dumps({
        "profile": {
            "real_name": name,
            "display_name": name
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

    print(json.dumps(result, indent=2))

    if not result.get("ok"):
        raise RuntimeError(f"Slack API error: {result}")

    print(f"Updated real and display names: {name}")


if __name__ == "__main__":
    name = get_countdown()
    update_slack_name(name, "SLACK_USER_TOKEN_1")
    update_slack_name(name, "SLACK_USER_TOKEN_2")

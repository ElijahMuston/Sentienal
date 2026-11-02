
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "sample_events.json"

USERS = ["alex", "sam", "jordan", "taylor", "system"]
IPS = [
    "192.0.2.10",
    "192.0.2.11",
    "192.0.2.12",
    "192.0.2.13",
    "192.0.2.14",
]

events = []

now = datetime.now(timezone.utc)

for i in range(100):
    event_type = random.choice([
        "login",
        "login",
        "application_error",
        "network",
    ])

    if event_type == "login":
        status = random.choice(["success", "success", "failed"])
    elif event_type == "application_error":
        status = "error"
    else:
        status = "connected"

    event = {
        "timestamp": (
            now - timedelta(minutes=100 - i)
        ).isoformat(),
        "event_type": event_type,
        "username": random.choice(USERS),
        "source_ip": random.choice(IPS),
        "status": status,
    }

    events.append(event)

with OUTPUT_FILE.open("w", encoding="utf-8") as file:
    json.dump(events, file, indent=2)

print(f"Generated {len(events)} synthetic events.")
print(f"Saved to: {OUTPUT_FILE}")

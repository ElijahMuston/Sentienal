
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Store generated events in the project's data folder.
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

events = [
    {
        "event_type": "login",
        "username": "alex",
        "source_ip": "192.0.2.10",
        "status": "success",
    },
    {
        "event_type": "login",
        "username": "sam",
        "source_ip": "192.0.2.11",
        "status": "failed",
    },
    {
        "event_type": "application_error",
        "username": "system",
        "source_ip": "192.0.2.12",
        "status": "error",
    },
    {
        "event_type": "network",
        "username": "system",
        "source_ip": "192.0.2.13",
        "status": "connected",
    },
    {
        "event_type": "login",
        "username": "sam",
        "source_ip": "192.0.2.11",
        "status": "failed",
    },
]

now = datetime.now(timezone.utc)

for index, event in enumerate(events):
    event["timestamp"] = (
        now - timedelta(minutes=len(events) - index)
    ).isoformat()

output_file = DATA_DIR / "sample_events.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(events, file, indent=2)

print(f"Generated {len(events)} synthetic events.")
print(f"Saved to: {output_file}")

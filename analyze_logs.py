
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("data") / "sample_events.json"

VALID_EVENT_TYPES = {
    "login",
    "application_error",
    "network",
}

VALID_STATUSES = {
    "success",
    "failed",
    "error",
    "connected",
}

REQUIRED_FIELDS = {
    "timestamp",
    "event_type",
    "username",
    "source_ip",
    "status",
}


def load_events(file_path):
    with file_path.open("r", encoding="utf-8") as file:
        events = json.load(file)

    if not isinstance(events, list):
        raise ValueError("Expected a list of events.")

    return events


def validate_event(event):
    if not isinstance(event, dict):
        return False, "Event must be an object."

    missing = REQUIRED_FIELDS - event.keys()

    if missing:
        return False, f"Missing fields: {', '.join(sorted(missing))}"

    for field in REQUIRED_FIELDS:
        if not isinstance(event[field], str) or not event[field].strip():
            return False, f"Invalid value for {field}."

    try:
        timestamp = datetime.fromisoformat(
            event["timestamp"].replace("Z", "+00:00")
        )
        if timestamp.tzinfo is None:
            return False, "Timestamp must include a timezone."
    except ValueError:
        return False, "Invalid timestamp."

    if event["event_type"] not in VALID_EVENT_TYPES:
        return False, "Unknown event type."

    if event["status"] not in VALID_STATUSES:
        return False, "Unknown status."

    return True, "Valid event."


def summarize_events(events):
    valid_events = []
    invalid_count = 0

    for index, event in enumerate(events, start=1):
        valid, reason = validate_event(event)

        if valid:
            valid_events.append(event)
        else:
            print(f"Invalid event #{index}: {reason}")
            invalid_count += 1

    event_counts = Counter(
        event["event_type"] for event in valid_events
    )

    print("\n=== SENTINEL LOG SUMMARY ===")
    print(f"Total events: {len(events)}")
    print(f"Valid events: {len(valid_events)}")
    print(f"Invalid events: {invalid_count}")

    print("\nEvents by type:")

    for event_type, count in sorted(event_counts.items()):
        print(f"  {event_type}: {count}")


def main():
    if not LOG_FILE.exists():
        print("Log file not found. Generate logs first.")
        return

    try:
        events = load_events(LOG_FILE)
        summarize_events(events)

    except (json.JSONDecodeError, ValueError, OSError) as error:
        print(f"Could not process logs: {error}")


if __name__ == "__main__":
    main()

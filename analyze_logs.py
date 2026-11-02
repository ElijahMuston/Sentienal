
import json
from collections import Counter
from pathlib import Path

LOG_FILE = Path("data") / "sample_events.json"


def load_events(file_path):
    """Load synthetic events from a JSON file."""
    with file_path.open("r", encoding="utf-8") as file:
        events = json.load(file)

    if not isinstance(events, list):
        raise ValueError("Expected a JSON list of events.")

    return events


def summarize_events(events):
    """Print a summary of the events."""
    event_counts = Counter()
    status_counts = Counter()

    for event in events:
        event_counts[event.get("event_type", "unknown")] += 1
        status_counts[event.get("status", "unknown")] += 1

    print("\n=== SENTINEL LOG SUMMARY ===")
    print(f"Total events: {len(events)}")

    print("\nEvents by type:")
    for event_type, count in sorted(event_counts.items()):
        print(f"  {event_type}: {count}")

    print("\nEvents by status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")


def main():
    if not LOG_FILE.exists():
        print(f"Log file not found: {LOG_FILE}")
        print("Run python generate_logs.py first.")
        return

    try:
        events = load_events(LOG_FILE)
        summarize_events(events)
    except (json.JSONDecodeError, ValueError) as error:
        print(f"Could not process log file: {error}")


if __name__ == "__main__":
    main()

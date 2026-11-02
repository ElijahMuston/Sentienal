
import unittest

from analyze_logs import validate_event


class TestEventValidation(unittest.TestCase):

    def setUp(self):
        self.valid_event = {
            "timestamp": "2026-11-02T12:00:00+00:00",
            "event_type": "login",
            "username": "alex",
            "source_ip": "192.0.2.10",
            "status": "success",
        }

    def test_valid_event(self):
        valid, message = validate_event(self.valid_event)
        self.assertTrue(valid)

    def test_missing_timestamp(self):
        event = self.valid_event.copy()
        del event["timestamp"]

        valid, message = validate_event(event)
        self.assertFalse(valid)

    def test_invalid_timestamp(self):
        event = self.valid_event.copy()
        event["timestamp"] = "not-a-date"

        valid, message = validate_event(event)
        self.assertFalse(valid)

    def test_unknown_event_type(self):
        event = self.valid_event.copy()
        event["event_type"] = "unknown"

        valid, message = validate_event(event)
        self.assertFalse(valid)

    def test_unknown_status(self):
        event = self.valid_event.copy()
        event["status"] = "unknown"

        valid, message = validate_event(event)
        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()

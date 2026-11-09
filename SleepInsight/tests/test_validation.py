import unittest
from backend.validators import validate_sleep_payload, validate_screen_payload


class ValidationTests(unittest.TestCase):
    def test_sleep_quality_range(self):
        with self.assertRaises(ValueError):
            validate_sleep_payload({
                "sleep_date": "2026-08-01", "bedtime": "23:00", "wake_time": "07:00",
                "latency_minutes": 20, "awakenings": 1, "quality": 6
            })

    def test_negative_latency_rejected(self):
        with self.assertRaises(ValueError):
            validate_sleep_payload({
                "sleep_date": "2026-08-01", "bedtime": "23:00", "wake_time": "07:00",
                "latency_minutes": -1, "awakenings": 1, "quality": 4
            })

    def test_prebed_screen_not_more_than_total(self):
        with self.assertRaises(ValueError):
            validate_screen_payload({"event_date": "2026-08-01", "total_minutes": 50, "pre_bed_minutes": 70})


if __name__ == "__main__":
    unittest.main()

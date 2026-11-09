import unittest
from datetime import date
from backend.services.sleep_calculator import calculate_sleep_metrics, normalize_bedtime_minutes, circular_distance_minutes


class SleepCalculatorTests(unittest.TestCase):
    def test_normal_sleep(self):
        result = calculate_sleep_metrics(date(2026, 8, 1), "22:30", "06:30", 0)
        self.assertEqual(result["duration_minutes"], 480)

    def test_cross_midnight_with_latency(self):
        result = calculate_sleep_metrics(date(2026, 8, 1), "23:30", "06:30", 30)
        self.assertEqual(result["duration_minutes"], 390)

    def test_midnight_normalization(self):
        self.assertEqual(normalize_bedtime_minutes("00:10"), 1450)
        self.assertEqual(normalize_bedtime_minutes("23:50"), 1430)

    def test_circular_distance(self):
        self.assertEqual(circular_distance_minutes(1430, 10), 20)

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            calculate_sleep_metrics(date(2026, 8, 1), "21:00", "22:00", 90)


if __name__ == "__main__":
    unittest.main()

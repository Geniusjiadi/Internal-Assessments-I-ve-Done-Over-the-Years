import unittest
from datetime import date, timedelta
from backend.services.analytics_service import build_analytics
from backend.services.pattern_detector import detect_patterns


class PatternTests(unittest.TestCase):
    def test_screen_and_latency_patterns(self):
        rows = []
        for i in range(14):
            rows.append({
                "sleep_date": (date(2026,7,1)+timedelta(days=i)).isoformat(),
                "bedtime":"23:30",
                "wake_time":"07:00",
                "duration_minutes":480 if i < 7 else 430,
                "sleep_midpoint_minutes":195,
                "quality":2 if i >= 7 else 4,
                "latency_minutes":40 if i >= 7 else 15,
                "pre_bed_screen_minutes":90 if i >= 7 else 20,
                "late_caffeine_mg":100 if i % 2 == 0 else 0,
                "exercise_minutes":20,
            })
        analytics = build_analytics(rows)
        patterns = detect_patterns(rows, analytics)
        ids = {p["rule_id"] for p in patterns}
        self.assertIn("declining_sleep_duration", ids)
        self.assertIn("high_prebed_screen", ids)
        self.assertIn("high_sleep_latency", ids)
        self.assertIn("repeated_late_caffeine", ids)


if __name__ == "__main__":
    unittest.main()

import unittest
from datetime import date, timedelta
from backend.services.trend_analyzer import rolling_period_comparison, regularity_analysis, weekday_weekend_analysis
from backend.services.analytics_service import build_analytics


def row(i, duration, bedtime="23:30", wake="07:00", quality=4, latency=15, screen=30, caffeine=0):
    d = date(2026, 7, 1) + timedelta(days=i)
    return {
        "sleep_date": d.isoformat(),
        "bedtime": bedtime,
        "wake_time": wake,
        "duration_minutes": duration,
        "sleep_midpoint_minutes": 3 * 60 + 15,
        "quality": quality,
        "latency_minutes": latency,
        "pre_bed_screen_minutes": screen,
        "late_caffeine_mg": caffeine,
        "exercise_minutes": 30,
    }


class AnalyticsTests(unittest.TestCase):
    def test_rolling_change(self):
        rows = [row(i, 480 if i < 7 else 420) for i in range(14)]
        result = rolling_period_comparison(rows, "duration_minutes", 7)
        self.assertEqual(result["current"], 420)
        self.assertEqual(result["previous"], 480)
        self.assertEqual(result["change"], -60)

    def test_regularity_midnight_wrap(self):
        rows = [
            row(0, 450, "23:50"),
            row(1, 450, "00:10"),
            row(2, 450, "23:40"),
            row(3, 450, "00:05"),
        ]
        result = regularity_analysis(rows)
        self.assertLess(result["bedtime_sd"], 20)

    def test_full_analytics(self):
        rows = [row(i, 450 + i, quality=3 + (i % 3), screen=20 + i * 2) for i in range(20)]
        result = build_analytics(rows)
        self.assertEqual(result["record_count"], 20)
        self.assertIn("correlations", result)
        self.assertIsNotNone(result["latest_sleep_score"])


if __name__ == "__main__":
    unittest.main()

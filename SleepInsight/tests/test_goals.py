import unittest
from datetime import date, timedelta
from backend.services.goal_engine import goal_progress, adaptive_goal_suggestion


class GoalTests(unittest.TestCase):
    def setUp(self):
        start = date(2026, 8, 1)
        self.rows = []
        for i in range(7):
            self.rows.append({
                "sleep_date": (start + timedelta(days=i)).isoformat(),
                "duration_minutes": 470 if i < 5 else 420,
                "bedtime": "23:30" if i < 5 else "00:20",
                "latency_minutes": 15,
                "pre_bed_screen_minutes": 35 if i < 5 else 80,
            })

    def test_goal_progress(self):
        goal = {
            "goal_type":"minimum_sleep_minutes","target_value":450,"target_time":None,
            "target_nights_per_week":5,"start_date":"2026-08-01","end_date":None,
            "adaptive_enabled":True,
        }
        progress = goal_progress(goal, self.rows)
        self.assertEqual(progress["met_nights"], 5)
        self.assertEqual(progress["completion_percent"], 100.0)
        suggestion = adaptive_goal_suggestion(goal, progress)
        self.assertEqual(suggestion["suggested_target"], 465.0)


if __name__ == "__main__":
    unittest.main()

import unittest
from backend.services.recommendation_engine import generate_recommendations


class RecommendationTests(unittest.TestCase):
    def test_priority_sort_and_goal_relevance(self):
        patterns = [
            {"rule_id":"high_prebed_screen","severity":0.8,"title":"Screen","reason":"High screen","confidence":"moderate","evidence":{}},
            {"rule_id":"high_sleep_latency","severity":0.5,"title":"Latency","reason":"High latency","confidence":"moderate","evidence":{}},
        ]
        correlations = [
            {"x":"pre_bed_screen_minutes","y":"quality","rho":-0.7,"sample_size":30,"label":"Screen vs quality","confidence":"moderate"},
        ]
        goals = [{"goal_type":"prebed_screen_max","active":True}]
        recs = generate_recommendations(patterns, correlations, goals)
        self.assertEqual(recs[0]["rule_id"], "high_prebed_screen")
        self.assertGreater(recs[0]["priority_score"], recs[1]["priority_score"])
        self.assertIn("ρ=", recs[0]["reason"])


if __name__ == "__main__":
    unittest.main()

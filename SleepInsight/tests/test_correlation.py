import unittest
from backend.services.correlation_engine import rank_data, spearman_rank_correlation, confidence_from_sample


class CorrelationTests(unittest.TestCase):
    def test_tied_ranks(self):
        self.assertEqual(rank_data([10, 20, 20, 40]), [1.0, 2.5, 2.5, 4.0])

    def test_perfect_negative(self):
        result = spearman_rank_correlation([1, 2, 3, 4], [8, 6, 4, 2])
        self.assertAlmostEqual(result["rho"], -1.0)

    def test_missing_pair_excluded(self):
        result = spearman_rank_correlation([1, None, 3, 4], [1, 2, 3, 4])
        self.assertEqual(result["sample_size"], 3)

    def test_confidence(self):
        self.assertEqual(confidence_from_sample(5), "insufficient")
        self.assertEqual(confidence_from_sample(20), "low")
        self.assertEqual(confidence_from_sample(40), "moderate")
        self.assertEqual(confidence_from_sample(70), "high")


if __name__ == "__main__":
    unittest.main()

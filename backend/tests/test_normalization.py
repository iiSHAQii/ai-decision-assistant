import unittest

from backend.services.normalization import min_max_normalize


class TestMinMaxNormalize(unittest.TestCase):
    def test_higher_is_better_basic(self):
        self.assertEqual(
            min_max_normalize([10.0, 20.0, 30.0], "higher_is_better"),
            [0.0, 0.5, 1.0],
        )

    def test_lower_is_better_inverts(self):
        self.assertEqual(
            min_max_normalize([10.0, 20.0, 30.0], "lower_is_better"),
            [1.0, 0.5, 0.0],
        )

    def test_all_equal_returns_half(self):
        self.assertEqual(
            min_max_normalize([5.0, 5.0, 5.0], "higher_is_better"),
            [0.5, 0.5, 0.5],
        )

    def test_all_none(self):
        self.assertEqual(
            min_max_normalize([None, None], "higher_is_better"),
            [None, None],
        )

    def test_mixed_none(self):
        self.assertEqual(
            min_max_normalize([10.0, None, 30.0], "higher_is_better"),
            [0.0, None, 1.0],
        )

    def test_single_value_treated_as_all_equal(self):
        self.assertEqual(
            min_max_normalize([42.0], "higher_is_better"),
            [0.5],
        )

    def test_already_normalized_passthrough(self):
        self.assertEqual(
            min_max_normalize([0.3, 0.7, 0.5], "already_normalized"),
            [0.3, 0.7, 0.5],
        )

    def test_already_normalized_clamps(self):
        self.assertEqual(
            min_max_normalize([-0.1, 0.5, 1.2], "already_normalized"),
            [0.0, 0.5, 1.0],
        )

    def test_already_normalized_with_none(self):
        self.assertEqual(
            min_max_normalize([0.3, None, 0.7], "already_normalized"),
            [0.3, None, 0.7],
        )


if __name__ == "__main__":
    unittest.main()

import unittest
from datetime import datetime

from data_analyzer.utils import compute_average_time


class TestUtils(unittest.TestCase):

    def test_empty_list(self):
        self.assertIsNone(compute_average_time([]), "Should return None for an empty list")

    def test_single_timestamp(self):
        timestamp = datetime.min.replace(hour=10, minute=30, second=0, microsecond=0).time()
        self.assertEqual(compute_average_time([timestamp]), timestamp,
                         "Should return the same time for a single timestamp")

    def test_multiple_timestamps(self):
        timestamp1 = datetime.min.replace(hour=1, minute=30, second=0, microsecond=0).time()  # 01:30 AM
        timestamp2 = datetime.min.replace(hour=12, minute=0, second=0, microsecond=0).time()  # 12:00 PM
        timestamp3 = datetime.min.replace(hour=18, minute=45, second=0, microsecond=0).time()  # 06:45 PM

        expected_time = datetime.min.replace(hour=10, minute=45, second=0, microsecond=0).time()

        self.assertEqual(compute_average_time([timestamp1, timestamp2, timestamp3]), expected_time,
                         "Should return the correct average time")

    def test_times_with_seconds(self):
        timestamp1 = datetime.min.replace(hour=10, minute=30, second=45, microsecond=0).time()  # 10:30:45
        timestamp2 = datetime.min.replace(hour=12, minute=0, second=30, microsecond=0).time()  # 12:00:30
        timestamp3 = datetime.min.replace(hour=14, minute=15, second=15, microsecond=0).time()  # 14:15:15

        expected_time = datetime.min.replace(hour=12, minute=15, second=30, microsecond=0).time()

        self.assertEqual(compute_average_time([timestamp1, timestamp2, timestamp3]), expected_time,
                         "Should return the correct average time")

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from habit import Habit

class TestHabit(unittest.TestCase):
    def setUp(self):
        # Two sample habits: one daily, one weekly
        self.daily = Habit("exercise", "daily")
        self.weekly = Habit("review finances", "weekly")

    @patch('builtins.print')
    def test_check_off_adds_today(self, mock_print):
        """check_off() should append today's date once."""
        self.daily.check_off()
        self.assertEqual(len(self.daily.completion_log), 1)
        self.assertEqual(self.daily.completion_log[0].date(), datetime.now().date())

    @patch('builtins.print')
    def test_uncheck_removes_today(self, mock_print):
        """uncheck() should remove today’s entry."""
        self.daily.check_off()
        self.assertEqual(len(self.daily.completion_log), 1)
        self.daily.uncheck()
        self.assertEqual(len(self.daily.completion_log), 0)

    @patch('builtins.print')
    def test_longest_streak_daily(self, mock_print):
        """get_longest_streak() should count consecutive daily entries."""
        now = datetime.now()
        # Create a 3-day streak
        self.daily.completion_log = [
            now,
            now - timedelta(days=1),
            now - timedelta(days=2),
        ]
        self.assertEqual(self.daily.get_longest_streak(), 3)

    @patch('builtins.print')
    def test_check_off_prevents_duplicates(self, mock_print):
        """Calling check_off twice in the same day/week should not add duplicates."""
        # Daily duplicate
        self.daily.check_off()
        self.daily.check_off()
        self.assertEqual(len(self.daily.completion_log), 1)

        # Weekly duplicate
        custom = datetime.now() - timedelta(days=2)
        self.weekly.check_off(custom)
        self.weekly.check_off(custom)
        self.assertEqual(len(self.weekly.completion_log), 1)

    @patch('builtins.print')
    def test_check_off_with_custom_date_weekly(self, mock_print):
        """check_off(date) should accept and log a custom date for weekly habits."""
        custom_date = datetime(2025, 7, 10)
        self.weekly.check_off(custom_date)
        self.assertEqual(len(self.weekly.completion_log), 1)
        self.assertEqual(self.weekly.completion_log[0].date(), custom_date.date())

if __name__ == "__main__":
    unittest.main()
# This code is a unit test for the Habit class, testing its methods and behaviors.
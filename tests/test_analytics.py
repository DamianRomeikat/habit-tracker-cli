import unittest
from datetime import datetime, timedelta
from analytics import get_streak_summary
from habit import Habit
from analytics import (
    get_all_habits,
    filter_habits_by_periodicity,
    calculate_streak_for_habit,
    calculate_longest_streaks,
)

class TestAnalytics(unittest.TestCase):

    def setUp(self):
        # Create some sample habits
        now = datetime.now()
        # Habit A: daily, 3-day streak
        self.hab_a = Habit("a", "daily")
        self.hab_a.completion_log = [
            now,
            now - timedelta(days=1),
            now - timedelta(days=2)
        ]
        # Habit B: daily, 5-day streak
        self.hab_b = Habit("b", "daily")
        self.hab_b.completion_log = [
            now,
            now - timedelta(days=1),
            now - timedelta(days=2),
            now - timedelta(days=3),
            now - timedelta(days=4)
        ]
        # Habit C: weekly, 2-week streak
        self.hab_c = Habit("c", "weekly")
        for wk in range(2):
            d = now - timedelta(weeks=wk)
            self.hab_c.completion_log.append(d)
        # Habit D: weekly, broken streak (gap)
        self.hab_d = Habit("d", "weekly")
        self.hab_d.completion_log = [
            now - timedelta(weeks=0),
            now - timedelta(weeks=2)
        ]

    def test_get_all_habits(self):
        names = get_all_habits([self.hab_a, self.hab_b, self.hab_c])
        self.assertEqual(names, ["a", "b", "c"])

    def test_filter_by_periodicity(self):
        mixed = [self.hab_a, self.hab_c, self.hab_b, self.hab_d]
        daily = filter_habits_by_periodicity(mixed, "daily")
        weekly = filter_habits_by_periodicity(mixed, "weekly")
        self.assertCountEqual([h.name for h in daily], ["a", "b"])
        self.assertCountEqual([h.name for h in weekly], ["c", "d"])

    def test_calculate_streak_for_habit(self):
        # Should delegate to get_current_streak (which is len(log) for now)
        self.assertEqual(calculate_streak_for_habit(self.hab_a), len(self.hab_a.completion_log))

    def test_calculate_longest_streaks_empty(self):
        self.assertEqual(calculate_longest_streaks([]), 0)

    def test_calculate_longest_streaks_nonempty(self):
        # h_b has 5 daily, h_c has 2 weekly, h_d has a broken weekly but two entries
            result = calculate_longest_streaks([self.hab_a, self.hab_b, self.hab_c, self.hab_d])
            # The longest streak is from hab_b (5)
            self.assertEqual(result, 5)
            
    # Test the summary function
    def test_get_streak_summary(self):
            habits = [self.hab_a, self.hab_b, self.hab_c]
            summary = get_streak_summary(habits)
    
            self.assertEqual(summary["total_habits"], 3)
            self.assertEqual(summary["longest_streak_overall"], 5)
            self.assertAlmostEqual(summary["average_streak"], 3.33, places=2) # Average of 3.33 from (3 + 5 + 2) / 3

if __name__ == "__main__":
    unittest.main()

import unittest
import os
import json
import tempfile
from datetime import datetime, timedelta

from habit import Habit
from habit_manager import HabitManager

class TestHabitManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary file path for JSON persistence tests
        self.tmp_fd, self.tmp_path = tempfile.mkstemp(suffix=".json")
        os.close(self.tmp_fd)
        # Ensure it starts empty
        try:
            os.remove(self.tmp_path)
        except FileNotFoundError:
            pass

        self.manager = HabitManager()

    def tearDown(self):
        # Clean up the temp file
        try:
            os.remove(self.tmp_path)
        except FileNotFoundError:
            pass

    def test_add_and_remove_habit(self):
        h1 = Habit("test1", "daily")
        h2 = Habit("test2", "weekly")

        self.manager.add_habit(h1)
        self.manager.add_habit(h2)
        self.assertEqual(len(self.manager.habits), 2)

        self.manager.remove_habit("test1")
        self.assertEqual(len(self.manager.habits), 1)
        self.assertEqual(self.manager.habits[0].name, "test2")

    def test_filter_by_periodicity(self):
        d1 = Habit("d", "daily")
        d2 = Habit("d2", "daily")
        w1 = Habit("w", "weekly")
        self.manager.add_habit(d1)
        self.manager.add_habit(d2)
        self.manager.add_habit(w1)

        daily = self.manager.get_habits_by_periodicity("daily")
        weekly = self.manager.get_habits_by_periodicity("weekly")
        self.assertCountEqual([h.name for h in daily], ["d", "d2"])
        self.assertEqual([h.name for h in weekly], ["w"])

    def test_get_longest_streaks(self):
        # create habits with known streaks
        h1 = Habit("h1", "daily")
        now = datetime.now()
        h1.completion_log = [now - timedelta(days=i) for i in range(3)]  # streak 3

        h2 = Habit("h2", "daily")
        h2.completion_log = [now - timedelta(days=i) for i in range(5)]  # streak 5

        self.manager.add_habit(h1)
        self.manager.add_habit(h2)
        self.assertEqual(self.manager.get_longest_streak(), 5)
        self.assertEqual(self.manager.get_longest_streak_for_habit("h1"), 3)
        self.assertIsNone(self.manager.get_longest_streak_for_habit("nope"))

    def test_save_and_load(self):
        # add a habit, save, then load into a new manager
        h = Habit("persist", "daily")
        h.completion_log = [datetime.now()]
        self.manager.add_habit(h)
        self.manager.save_to_file(self.tmp_path)

        mgr2 = HabitManager()
        mgr2.load_from_file(self.tmp_path)
        self.assertEqual(len(mgr2.habits), 1)
        loaded = mgr2.habits[0]
        self.assertEqual(loaded.name, "persist")
        self.assertEqual(loaded.periodicity, "daily")
        self.assertEqual(len(loaded.completion_log), 1)

    def test_load_or_create_sample_data(self):
        # Ensure no file exists
        try:
            os.remove(self.tmp_path)
        except FileNotFoundError:
            pass

        # Load or create sample data
        self.manager.load_or_create_sample_data(self.tmp_path)
        # Should have 5 habits
        names = sorted(h.name for h in self.manager.habits)
        # Our sample names: lowercase of your configured list
        expected = sorted([
            "morning walk",
            "journal for 10 minutes",
            "drink 2 liters of water",
            "plan weekly budget",
            "call a friend or family member"
        ])
        self.assertEqual(names, expected)

        # And now the file should exist
        self.assertTrue(os.path.exists(self.tmp_path))
        # And loading again should not re-create (just load)
        mgr2 = HabitManager()
        mgr2.load_or_create_sample_data(self.tmp_path)
        self.assertEqual(len(mgr2.habits), 5)

if __name__ == "__main__":
    unittest.main()

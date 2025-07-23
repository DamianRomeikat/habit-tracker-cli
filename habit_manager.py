import json
import os
from typing import List, Optional
from habit import Habit  # Import the Habit class for habit.py
from datetime import datetime, timedelta


class HabitManager:
    """
    Manages a list of habits and handles saving, loading, and operations on them.
    """

    def __init__(self):
        self.habits: List[Habit] = []

    def add_habit(self, habit: Habit):
        """
        Add a new habit to the list.

        Args:
            habit (Habit): The habit to add.
        """
        self.habits.append(habit)

    def remove_habit(self, name: str):
        """
        Remove a habit by its name.

        Args:
            name (str): The name of the habit to remove.
        """
        self.habits = [h for h in self.habits if h.name != name]

    def get_habits_by_periodicity(self, periodicity: str) -> List[Habit]:
        """
        Filter habits by periodicity.

        Args:
            periodicity (str): Either 'daily' or 'weekly'.

        Returns:
            List[Habit]: Matching habits.
        """
        return [h for h in self.habits if h.periodicity == periodicity]

    def get_longest_streak(self) -> Optional[int]:
        """
        Get the longest streak across all habits.

        Returns:
            Optional[int]: The maximum streak found, or None if no habits exist.
        """
        if not self.habits:
            return None
        return max(h.get_current_streak() for h in self.habits)

    def get_longest_streak_for_habit(self, name: str) -> Optional[int]:
        """
        Get the longest streak for a specific habit by name.

        Args:
            name (str): Name of the habit.

        Returns:
            Optional[int]: The streak, or None if the habit was not found.
        """
        for h in self.habits:
            if h.name == name:
                return h.get_current_streak()
        return None

    def save_to_file(self, filename: str = "habits.json"):
        """
        Save habits to a JSON file.

        Args:
            filename (str): File name to save to.
        """
        with open(filename, "w") as f:
            json.dump([{
                "name": h.name,
                "periodicity": h.periodicity,
                "created_at": h.created_at.isoformat(),
                "completion_log": [dt.isoformat() for dt in h.completion_log]
            } for h in self.habits], f, indent=4)

    def load_from_file(self, filename: str = "habits.json"):
        """
        Load habits from a JSON file.

        Args:
            filename (str): File name to load from.
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.habits = []
                for item in data:
                    habit = Habit(item["name"], item["periodicity"])
                    habit.created_at = datetime.fromisoformat(item["created_at"])
                    # Handle missing completion_log gracefully
                    completion_log = item.get("completion_log", [])
                    habit.completion_log = [datetime.fromisoformat(dt) for dt in completion_log]
                    self.habits.append(habit)
        except FileNotFoundError:
            print("No saved habits found. Starting with an empty list.")

    def load_or_create_sample_data(self, session_date: datetime, filename: str = "habits.json"):
        """
        Load habit data from file or create predefined sample data if file is missing.
        """
        if os.path.exists(filename):
            self.load_from_file(filename)
            return

        print("📦 No habits file found — creating sample data...")

        # Sample habits
        daily_habits = ["Morning Walk", "Journal for 10 Minutes", "Drink 2 Liters of Water"]
        weekly_habits = ["Plan Weekly Budget", "Call a Friend or Family Member"]

        now = session_date  # ✅ use the date passed from main.py

        # Create daily habits with 28 days of data
        for name in daily_habits:
            habit = Habit(name.lower(), "daily")
            for days_ago in range(28):
                habit.completion_log.append(now - timedelta(days=days_ago))
            self.add_habit(habit)

    # Create weekly habits with 4 weeks of data
        for name in weekly_habits:
            habit = Habit(name.lower(), "weekly")
            for weeks_ago in range(4):
                # Always add log on a fixed weekday (e.g., Sunday = 6)
                weekly_date = (now - timedelta(weeks=weeks_ago)).replace(hour=9, minute=0, second=0, microsecond=0)
                while weekly_date.weekday() != 6:  # 6 = Sunday
                    weekly_date -= timedelta(days=1)
                habit.completion_log.append(weekly_date)
            self.add_habit(habit)

        self.save_to_file(filename)
        print("✅ Sample habits created and saved.")

from datetime import timedelta



"""
# test the HabitManager class manually
if __name__ == "__main__":
    print("✅ Starting HabitManager test...")

    from datetime import timedelta

    # Create the manager
    manager = HabitManager()

    # Create and check off some habits
    habit1 = Habit("Read", "daily")
    habit1.check_off()

    habit2 = Habit("Workout", "weekly")
    habit2.check_off(datetime.now() - timedelta(days=7))

    # Add them to the manager
    manager.add_habit(habit1)
    manager.add_habit(habit2)

    # Save to file
    manager.save_to_file()

    # Reload and verify
    manager = HabitManager()
    manager.load_from_file()

    # Display loaded habits
    for h in manager.habits:
        print(f"Habit: {h.name}, Periodicity: {h.periodicity}, Completions: {len(h.completion_log)}")

    # Filter test
    daily = manager.get_habits_by_periodicity("daily")
    print("Daily Habits:", [h.name for h in daily])

    # Streak test
    print("Longest overall streak:", manager.get_longest_streak())
    print("Streak for 'Read':", manager.get_longest_streak_for_habit("Read"))
"""
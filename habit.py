from datetime import datetime, timedelta
from typing import List, Optional

class Habit:
    """
    Represents a single habit the user wants to track.
    """

    def __init__(self, name: str, periodicity: str):
        """
        Initialize a new habit with name and periodicity.

        Args:
            name (str): Name of the habit.
            periodicity (str): 'daily' or 'weekly'.
        """
        self.name = name
        self.periodicity = periodicity  # Should be 'daily' or 'weekly'
        self.created_at = datetime.now()  # Timestamp when the habit was created
        self.completion_log: List[datetime] = []  # Log of datetime entries for each completed check-off

    def check_off(self, date: Optional[datetime] = None):
        """
        Mark the habit as completed for the given date or today.

        Prevents duplicate check-ins for the same day (daily) or week (weekly).

        Args:
            date (Optional[datetime]): The date to check off. Defaults to now.
        """
        check_date = date or datetime.now()

        # Check if this habit has already been checked off for this period
        for log_date in self.completion_log:
            if self.periodicity == 'daily' and log_date.date() == check_date.date():
                print("Habit already checked off today.")
                return
            elif self.periodicity == 'weekly':
                # Compare ISO week number and year
                if (log_date.isocalendar()[1] == check_date.isocalendar()[1] and
                    log_date.year == check_date.year):
                    print("Habit already checked off this week.")
                    return
                
                
        # No duplicate found; add the completion timestamp
        self.completion_log.append(check_date)
        print("Habit checked off successfully.")

    def uncheck(self):
        """
        Remove today's (for daily) or this week's (for weekly) check-off from the log.
        """
        now = datetime.now()
        new_log = []

        for log in self.completion_log:
            if self.periodicity == "daily" and log.date() == now.date():
                continue  # skip today's log
            elif self.periodicity == "weekly":
                same_week = log.isocalendar()[1] == now.isocalendar()[1]
                same_year = log.year == now.year
                if same_week and same_year:
                    continue  # skip this week's log
            new_log.append(log)

        self.completion_log = new_log
        print("Habit unchecked for current period.")


    def get_current_streak(self) -> int:
        """
        Calculate the current streak based on periodicity.

        NOTE: This is a placeholder and will be implemented in detail later.

        Returns:
            int: Current streak length (currently just the count of completions).
        """
        return len(self.completion_log)
    
    def get_longest_streak(self) -> int:
        """
        Calculate the longest uninterrupted streak of completions.

        Works for both 'daily' and 'weekly' habits.
        """
        if not self.completion_log:
            return 0

        # Sort log in ascending order
        sorted_log = sorted(self.completion_log)
        longest = 1
        current = 1

        for i in range(1, len(sorted_log)):
            prev = sorted_log[i - 1]
            curr = sorted_log[i]

            if self.periodicity == "daily":
                expected = prev.date() + timedelta(days=1)
                if curr.date() == expected:
                    current += 1
                    longest = max(longest, current)
                elif curr.date() > expected:
                    current = 1  # Streak broken
            elif self.periodicity == "weekly":
                prev_year, prev_week, _ = prev.isocalendar()
                curr_year, curr_week, _ = curr.isocalendar()
                if (curr_year == prev_year and curr_week == prev_week + 1) or \
                    (curr_year == prev_year + 1 and prev_week == 52 and curr_week == 1):
                    current += 1
                    longest = max(longest, current)
                elif (curr_year > prev_year) or (curr_week > prev_week + 1):
                    current = 1

        return longest

    def is_broken(self, period_start: datetime, period_end: datetime) -> bool:
        """
        Check if the habit was broken during the given time period.

        Args:
            period_start (datetime): Start of the time window.
            period_end (datetime): End of the time window.

        Returns:
            bool: True if no completion happened during the time period, else False.
        """
        for log in self.completion_log:
            if period_start <= log <= period_end:
                return False  # Habit was completed at least once in the period
        return True  # No completion found in the specified period
    
    
    

"""
# Test the Habit class manually

if __name__ == "__main__":
    # Create a habit
    habit = Habit("Exercise", "daily")

    # Check it off today
    habit.check_off()  # Should print: Habit checked off successfully.

    # Try to check it off again on the same day
    habit.check_off()  # Should print: Habit already checked off today.

    # Print the current streak (will just be number of completions for now)
    print("Current streak:", habit.get_current_streak())

    # Simulate checking for a broken period
    start = datetime.now() - timedelta(days=3)
    end = datetime.now()
    print("Is broken in last 3 days:", habit.is_broken(start, end))  # Should be False

    # Add a check-off from 2 days ago to simulate manual entry
    habit.check_off(datetime.now() - timedelta(days=2))
    
    # Test get_longest_streak (currently same as get_current_streak)
    print("Longest streak:", habit.get_longest_streak())
"""


from typing import List
from habit import Habit
from functools import reduce

def get_all_habits(habits: List[Habit]) -> List[str]:
    """
    Return the names of all habits.
    """
    return list(map(lambda h: h.name, habits))


def filter_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """
    Filter habits by 'daily' or 'weekly'.
    """
    return list(filter(lambda h: h.periodicity == periodicity, habits))


def calculate_streak_for_habit(habit: Habit) -> int:
    """
    Get the current streak for a single habit.
    """
    return habit.get_current_streak()


def calculate_longest_streaks(habits: List[Habit]) -> int:
    """
    Get the longest streak across all habits.
    """
    if not habits:
        return 0
    return max((h.get_longest_streak() for h in habits), default=0)

def get_streak_summary(habits: List[Habit]) -> dict:
    """
    Return a summary dictionary of streak analytics across all habits.

    Keys:
    - total_habits: total number of tracked habits
    - longest_streak_overall: the highest single habit streak
    - average_streak: mean of all longest streaks
    """
    if not habits:
        return {"total_habits": 0, "longest_streak_overall": 0, "average_streak": 0.0}

    total = len(habits)
    longest = calculate_longest_streaks(habits)
    average = round(
        sum(h.get_longest_streak() for h in habits) / total, 2
    )

    return {
        "total_habits": total,
        "longest_streak_overall": longest,
        "average_streak": average,
    }

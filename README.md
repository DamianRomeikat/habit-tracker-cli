 Habit Tracker CLI
A comprehensive and user-friendly Command Line Interface (CLI) application for tracking habits, built using Python. This project was developed for the IU course **Object-Oriented and Functional Programming with Python (DLBDSOOFPP01)**.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Current Features
- **Daily & Weekly Habit Tracking:** Track habits based on daily or weekly periodicity.
- **Habit Management:** Add, remove, check, or uncheck habits easily from the menu.
- **Automatic Streak Tracking:** View current and longest streaks for each habit.
- **Simulated Checkboxes:** User-friendly interface with simulated checkboxes (`[x]`, `[ ]`) to indicate habit completion status.
- **Filtering & Sorting:** Filter habits by periodicity and sort by the longest streak.
- **Functional Analytics Module:** Utilize Python’s functional programming (`map`, `filter`, `reduce`) for habit analysis.
- **Data Persistence:** Habits are stored persistently in a JSON file (`habits.json`).
- **Sample Data Generation:** Automatically generates realistic sample data for easy initial use.
- **Date Flexibility:** Allows users to select a custom date or default to the current date for habit management.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Project Structure:

habit_tracker/
├── analytics.py
├── habit.py
├── habit_manager.py
├── main.py
├── habits.json (Automatically added on startup of tracker)
├── tests/
│ ├── test_habit.py
│ ├── test_habit_manager.py
│ └── test_analytics.py
├── README.md
└── requirements.txt

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

 ⚙️ Installation

### Requirements

- Python 3.10 or higher (developed with Python 3.13.5)
- `tabulate` module

Install the required dependencies using:

TRun the following in your terminal:

py -m pip install -r requirements.txt
 or
py -m pip install tabulate

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Running the app

from the projects root directory, please run the following in the terminal:

py main.py

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Usage display
when main.py is running, the following cli will generate:

📅 Welcome to the Habit Tracker!
Use today's date? (Y/n): Y
📌 Using today's date: 2025-07-21
📦 No habits file found — creating sample data...
✅ Sample habits created and saved.

📌 Your Habits:
╒═════╤═════════╤════════════════════════════════╤════════╤═══════════════╤══════════════════╤═════════════╕
│   # │ check   │ Habit                          │ Type   │   Completions │   Longest Streak │ Last Done   │
╞═════╪═════════╪════════════════════════════════╪════════╪═══════════════╪══════════════════╪═════════════╡
│   1 │ [x]     │ Morning Walk                   │ daily  │            28 │               28 │ 2025-06-24  │
├─────┼─────────┼────────────────────────────────┼────────┼───────────────┼──────────────────┼─────────────┤
│   2 │ [x]     │ Journal For 10 Minutes         │ daily  │            28 │               28 │ 2025-06-24  │
├─────┼─────────┼────────────────────────────────┼────────┼───────────────┼──────────────────┼─────────────┤
│   3 │ [x]     │ Drink 2 Liters Of Water        │ daily  │            28 │               28 │ 2025-06-24  │
├─────┼─────────┼────────────────────────────────┼────────┼───────────────┼──────────────────┼─────────────┤
│   4 │ [ ]     │ Plan Weekly Budget             │ weekly │             4 │                4 │ 2025-06-29  │
├─────┼─────────┼────────────────────────────────┼────────┼───────────────┼──────────────────┼─────────────┤
│   5 │ [ ]     │ Call A Friend Or Family Member │ weekly │             4 │                4 │ 2025-06-29  │
╘═════╧═════════╧════════════════════════════════╧════════╧═══════════════╧══════════════════╧═════════════╛

Menu:
1. Add a new habit
2. Remove a habit
3. Check/Uncheck off a habit
4. Show habits by periodicity
5. Show habits by longest streak
6. Show missed habits for this period
0. Exit
Enter your choice:

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Unit testing

To run all unit tests, showing visual output, please insert the following into the console:

py -m unittest discover -s tests -p "test_*.py"

To buffer out all stout outputs (all print()), please insert -b at the end of the expression

To suppress all outputs and only display succession time please insert -q at the end of the expression

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author

Damian Romeikat

Matriculation number: 102203512

Course: DLBDSOOFPP01 - Object-Oriented and Functional Programming with Python

GitHub repository:https://github.com/DamianRomeikat/habit-tracker-cli.git

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
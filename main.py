from habit_manager import HabitManager
from habit import Habit
import os
import sys
from datetime import datetime, timedelta
from tabulate import tabulate

def get_streak_summary(habits):
    summary = {
        "total_habits": len(habits),
        "total_completions": sum(len(h.completion_log) for h in habits),
        "longest_streak": max((h.get_longest_streak() for h in habits), default=0),
        "average_streak": round(sum(h.get_longest_streak() for h in habits) / len(habits), 2) if habits else 0
    }
    return summary

def print_menu():
    print("\nMenu:")
    print("1. Add a new habit")
    print("2. Remove a habit")
    print("3. Check/Uncheck off a habit")
    print("4. Show habits by periodicity")
    print("5. Show habits by longest streak")
    print("6. Show missed habits for this period")
    print("7. Show overall streak summary")
    print("0. Exit")

def main():
    
        # Ask user for a working date
    print("📅 Welcome to the Habit Tracker!")
    use_today = input("Use today's date? (Y/n): ").strip().lower()

    if use_today == "n":
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            session_date = datetime.strptime(date_str, "%Y-%m-%d")
            print(f"📌 Using custom date: {session_date.date()}")
        except ValueError:
            print("❌ Invalid date format. Using today instead.")
            session_date = datetime.now()
    else:
        session_date = datetime.now()
        print(f"📌 Using today's date: {session_date.date()}")


    manager = HabitManager()
    manager.load_or_create_sample_data(session_date)  # Load from file or generate sample habits if file doesn't exist

    while True:
        # 📌 Show current habits with simulated checkboxes
        if manager.habits:
            print("\n📌 Your Habits:")

            table_data = []
            now = session_date

            for idx, h in enumerate(manager.habits, 1):
                is_checked = False
                last_date = h.completion_log[-1].date() if h.completion_log else "N/A"

                for log in h.completion_log:
                    if h.periodicity == "daily" and log.date() == now.date():
                        is_checked = True
                        break
                    elif h.periodicity == "weekly" and log.isocalendar()[1] == now.isocalendar()[1] and log.year == now.year:
                        is_checked = True
                        break

                checkbox = "[x]" if is_checked else "[ ]"
                table_data.append([
                    idx,
                    checkbox,
                    h.name.title(),
                    h.periodicity,
                    len(h.completion_log),
                    h.get_longest_streak(),
                    last_date
                ])

            headers = ["#", "check", "Habit", "Type", "Completions", "Longest Streak", "Last Done"]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        else:
            print("\n📭 You have no habits yet.")

        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter habit name: ").strip().lower()
            periodicity = input("Enter periodicity (daily/weekly): ").lower()
            if periodicity not in ["daily", "weekly"]:
                print("Invalid periodicity.")
            else:
                habit = Habit(name, periodicity)
                manager.add_habit(habit)
                manager.save_to_file()
                print("✅ Habit added.")

        elif choice == "2":
            name = input("Enter the name of the habit to delete: ").strip().lower()
            manager.remove_habit(name)
            manager.save_to_file()
            print("🗑️ Habit removed.")

        elif choice == "3":
            if not manager.habits:
                print("No habits to update.")
            else:
                try:
                    index_input = input("Enter the number of the habit to toggle: ").strip()
                    if not index_input.isdigit():
                        print("❌ Please enter a valid number.")
                        continue
                    index = int(index_input) - 1
                    if index < 0 or index >= len(manager.habits):
                        print("❌ Number out of range.")
                        continue
                    habit = manager.habits[index]

                    print(f"🔁 Selected: {habit.name.title()} ({habit.periodicity})")

                    now = session_date
                    # Check if the habit is already checked for today
                    # Simulate checking/unchecking based on periodicity
                    is_checked = False

                    for log in habit.completion_log:
                        if habit.periodicity == "daily" and log.date() == now.date():
                            is_checked = True
                            break
                        elif habit.periodicity == "weekly":
                            if log.isocalendar()[1] == now.isocalendar()[1] and log.year == now.year:
                                is_checked = True
                                break

                    if is_checked:
                        habit.uncheck()
                        print(f"❌ Unchecked {habit.name} for this {habit.periodicity}.")
                    else:
                        habit.check_off(session_date)
                        print(f"✔️ Checked off {habit.name} for {session_date.date()}.")
                except Exception as e:
                    print(f"An error occurred: {e}")
        elif choice == "4":
            periodicity = input("Enter periodicity to filter by (daily/weekly): ").lower()
            if periodicity not in ["daily", "weekly"]:
                print("Invalid periodicity.")
            else:
                filtered = manager.get_habits_by_periodicity(periodicity)
                if not filtered:
                    print("No habits found for this periodicity.")
                for h in filtered:
                    print(f"📌 {h.name} – {len(h.completion_log)} completions")
                    
        elif choice == "5":
            if not manager.habits:
                print("No habits to sort.")
            else:
                sorted_habits = sorted(manager.habits, key=lambda h: h.get_longest_streak(), reverse=True)
                print("\n🏆 Habits Sorted by Longest Streak:")
                for h in sorted_habits:
                    print(f"- {h.name.title()} ({h.periodicity}) – Longest streak: {h.get_longest_streak()}")

        elif choice == "6":
            missed = []
            now = session_date
            # Check for missed habits

            for habit in manager.habits:
                is_checked = False
                for log in habit.completion_log:
                    if habit.periodicity == "daily" and log.date() == now.date():
                        is_checked = True
                        break
                    elif habit.periodicity == "weekly":
                        if log.isocalendar()[1] == now.isocalendar()[1] and log.year == now.year:
                            is_checked = True
                            break
                if not is_checked:
                    missed.append(habit)

            if missed:
                print("\n❌ Missed Habits:")
                for h in missed:
                    print(f"- {h.name.title()} ({h.periodicity})")
            else:
                print("\n✅ No missed habits. Good job!")

        elif choice == "7":
            summary = get_streak_summary(manager.habits)
            print("\n📊 Streak Summary:")
            for key, value in summary.items():
                print(f"{key.replace('_', ' ').title()}: {value}")


        elif choice == "0":
            print("👋 Goodbye!")
            sys.exit()

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

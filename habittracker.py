import json
import os
from datetime import datetime

DATA_FILE = "habits.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_habit(data):
    habit_name = input("Enter the new habit name: ").strip()
    if habit_name in data:
        print("Habit already exists!")
    else:
        data[habit_name] = {
            "streak": 0,
            "last_completed": "",
            "log": []
        }
        print(f"Habit '{habit_name}' added!")

def mark_habit_done(data):
    if not data:
        print("No habits found! Add a habit first.")
        return

    print("\nYour Habits:")
    for i, habit in enumerate(data.keys()):
        print(f"{i+1}. {habit}")

    try:
        choice = int(input("Select a habit number to mark as done: ")) - 1
        habit_name = list(data.keys())[choice]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    if data[habit_name]["last_completed"] == today:
        print("You’ve already marked this habit today!")
        return

    # Update streak
    last_date = data[habit_name]["last_completed"]
    if last_date:
        last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
        if (datetime.now() - last_date_obj).days == 1:
            data[habit_name]["streak"] += 1
        else:
            data[habit_name]["streak"] = 1
    else:
        data[habit_name]["streak"] = 1

    data[habit_name]["last_completed"] = today
    data[habit_name]["log"].append(today)
    print(f"Habit '{habit_name}' marked as done today!")

def view_habits(data):
    if not data:
        print("No habits to show.")
        return

    print("\nYour Habits:\n")
    for name, info in data.items():
        print(f" {name}")
        print(f"   ➤ Current Streak: {info['streak']} days")
        print(f"   ➤ Last Completed: {info['last_completed']}")
        print("-" * 40)

def main():
    data = load_data()
    while True:
        print("\n HABIT TRACKER ")
        print("1. Add New Habit")
        print("2. Mark Habit as Done")
        print("3. View Habits")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_habit(data)
        elif choice == "2":
            mark_habit_done(data)
        elif choice == "3":
            view_habits(data)
        elif choice == "4":
            save_data(data)
            print("Progress saved. Bye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

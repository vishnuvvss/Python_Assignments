import json
import os
import time
from datetime import datetime
import calendar

EXP_FILE = "expenses.json"
LOG_FILE = "app_log.txt"

def log_and_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n Running {func.__name__} at {start_dt}")

        result = func(*args, **kwargs)

        end = time.time()
        duration = end - start

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{start_dt} | {func.__name__} | {duration:.4f}s\n")

        return result
    return wrapper

def load_expenses():
    if not os.path.exists(EXP_FILE):
        with open(EXP_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        with open(EXP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        with open(EXP_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []


def save_expenses(data):
    with open(EXP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

@log_and_time
def add_expense():
    date_in = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not date_in:
        date_in = datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date_in, "%Y-%m-%d")
    except:
        print("Invalid date format.")
        return

    category = input("CEnter Category: ").strip()

    amt_in = input("Amount: ").strip()
    try:
        amount = float(amt_in)
    except:
        print("Invalid amount.")
        return

    description = input("Description (optional): ").strip()

    data = load_expenses()
    data.append({
        "date": date_in,
        "category": category,
        "amount": amount,
        "description": description
    })

    save_expenses(data)
    print(" Expense added successfully!")

@log_and_time
def view_expenses():
    data = load_expenses()

    if not data:
        print("No expenses found.")
        return

    data.sort(key=lambda x: x.get("date", ""))

    total = 0

    print("\nAll Expenses:")
    print("Date        | Category   | Amount | Description")
    print("-" * 55)

    for e in data:
        total += e.get("amount", 0)
        print(f"{e.get('date','')} | {e.get('category','')} | {e.get('amount',0)} | {e.get('description','')}")

    print("-" * 55)
    print(f"Total = {total}\n")

@log_and_time
def generate_monthly_summary():
    inp = input("Enter month and year (MM YYYY): ").strip().split()

    if len(inp) != 2:
        print("Invalid input.")
        return

    month, year = inp

    try:
        month = int(month)
        year = int(year)
    except:
        print("Invalid numbers.")
        return

    data = load_expenses()
    summary = {}
    total = 0

    for e in data:
        try:
            d = datetime.strptime(e.get("date", ""), "%Y-%m-%d")
        except:
            continue

        if d.month == month and d.year == year:
            c = e.get("category", "Other")
            summary[c] = summary.get(c, 0) + e.get("amount", 0)
            total += e.get("amount", 0)

    month_name = calendar.month_name[month]

    print(f"\n***** Monthly Summary: {month_name} {year} *****")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("-" * 40)
    print(f"Total: {total}")

    out_file = f"summary_{month_name}_{year}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "total": total}, f, indent=4)

    print(f"Summary exported to '{out_file}'.\n")

def main():
    while True:
        print("\n===== SMART EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Generate Monthly Summary")
        print("4. Exit")

        ch = input("Enter choice: ").strip()

        if ch == "1":
            add_expense()
        elif ch == "2":
            view_expenses()
        elif ch == "3":
            generate_monthly_summary()
        elif ch == "4":
            print("Exit...")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
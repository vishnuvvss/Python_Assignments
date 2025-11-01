def read_expenses(filename):
    records = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("Date"):
                    continue

                parts = line.split(",")
                if len(parts) != 3:
                    print(f"Skipping malformed line: {line}")
                    continue

                date = parts[0]
                category = parts[1]
                amount_str = parts[2]

                try:
                    amount = float(amount_str)
                except ValueError:
                    print(f"Invalid amount: {line}")
                    continue

                record = [date, category, amount]
                records.append(record)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return records


def calculate_summary(records, filter_category=None):
    total_expense = 0
    category_expense = {}
    daily_expense = {}

    for record in records:
        date = record[0]
        category = record[1]
        amount = record[2]

        if filter_category and category.lower() != filter_category.lower():
            continue

        total_expense += amount

        if category not in category_expense:
            category_expense[category] = 0
        category_expense[category] += amount

        if date not in daily_expense:
            daily_expense[date] = 0
        daily_expense[date] += amount

    if len(daily_expense) > 0:
        highest_day = max(daily_expense, key=daily_expense.get)
        highest_amount = daily_expense[highest_day]
    else:
        highest_day = "N/A"
        highest_amount = 0

    summary = {
        "total_expense": total_expense,
        "category_expense": category_expense,
        "highest_day": highest_day,
        "highest_amount": highest_amount
    }
    return summary

def write_summary(summary, filename):
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(" Expense Summary\n")
            file.write(f"Total Monthly Expense: Rs {int(summary['total_expense'])}\n\n")

            file.write("Category-wise Breakdown:\n")
            for category, amount in summary["category_expense"].items():
                file.write(f"{category:<15}: Rs {int(amount)}\n")

            file.write(f"\nHighest Spending Day: {summary['highest_day']} (Rs {int(summary['highest_amount'])})\n")
            file.write("\n")

        print(f"Summary saved to '{filename}'")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    input_file = input("Enter input CSV filename: ")
    output_file = input("Enter output summary filename: ")
    filter_category = input("Enter category to filter: (leave blank for all): ").strip()

    records = read_expenses(input_file)

    if len(records) == 0:
        print("No valid data found.")
        return

    summary = calculate_summary(records, filter_category if filter_category else None)
    write_summary(summary, output_file)


if __name__ == "__main__":
    main()
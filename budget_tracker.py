"""
budget_tracker.py

A simple command-line Budget Tracker for learning Python CRUD
(Create, Read, Update, Delete) operations, backed by a CSV file.

Built with only Python's standard library, so there is nothing to
pip install before you push this to GitHub.
"""

import csv
import os

DATA_FILE = "expenses.csv"
FIELDNAMES = ["id", "date", "category", "description", "amount"]


def init_file():
    """Create the CSV file with headers if it doesn't exist yet."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def _read_all():
    """Internal helper: read every row into a list of dicts."""
    init_file()
    with open(DATA_FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


def _write_all(rows):
    """Internal helper: overwrite the CSV file with the given rows."""
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


# ---------- CREATE ----------
def add_expense(date, category, description, amount):
    rows = _read_all()
    next_id = max((int(r["id"]) for r in rows), default=0) + 1
    rows.append({
        "id": str(next_id),
        "date": date,
        "category": category,
        "description": description,
        "amount": f"{float(amount):.2f}",
    })
    _write_all(rows)
    return next_id


# ---------- READ ----------
def list_expenses(category=None):
    rows = _read_all()
    if category:
        rows = [r for r in rows if r["category"].lower() == category.lower()]
    return rows


def get_expense(expense_id):
    for r in _read_all():
        if r["id"] == str(expense_id):
            return r
    return None


def total_spent(category=None):
    rows = list_expenses(category)
    return sum(float(r["amount"]) for r in rows)

def monthly_summary():
    """Group total spending by month (YYYY-MM)."""
    rows = _read_all()
    summary = {}
    for r in rows:
        month = r["date"][:7]  # takes "YYYY-MM" from "YYYY-MM-DD"
        summary[month] = summary.get(month, 0) + float(r["amount"])
    return summary


# ---------- UPDATE ----------
def update_expense(expense_id, **fields):
    rows = _read_all()
    updated = False
    for r in rows:
        if r["id"] == str(expense_id):
            for key, value in fields.items():
                if key in r and value is not None:
                    r[key] = str(value)
            updated = True
            break
    if updated:
        _write_all(rows)
    return updated


# ---------- DELETE ----------
def delete_expense(expense_id):
    rows = _read_all()
    new_rows = [r for r in rows if r["id"] != str(expense_id)]
    deleted = len(new_rows) != len(rows)
    if deleted:
        _write_all(new_rows)
    return deleted


# ---------- CLI ----------
def print_menu():
    print("\n=== Budget Tracker ===")
    print("1. Add expense")
    print("2. List expenses")
    print("3. Update expense")
    print("4. Delete expense")
    print("5. Show total spent")
    print("6. Monthly summary")
    print("7. Exit")

def run_cli():
    init_file()
    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            date = input("Date (YYYY-MM-DD): ")
            category = input("Category (e.g. Food, Rent): ")
            description = input("Description: ")
            amount = input("Amount: ")
            new_id = add_expense(date, category, description, amount)
            print(f"Added expense #{new_id}")

        elif choice == "2":
            category = input("Filter by category (leave blank for all): ").strip() or None
            for r in list_expenses(category):
                print(f"#{r['id']} | {r['date']} | {r['category']:12} | "
                      f"{r['description']:20} | {r['amount']}")

        elif choice == "3":
            expense_id = input("Expense ID to update: ")
            field = input("Field to change (date/category/description/amount): ").strip()
            value = input("New value: ")
            print("Updated." if update_expense(expense_id, **{field: value}) else "Not found.")

        elif choice == "4":
            expense_id = input("Expense ID to delete: ")
            print("Deleted." if delete_expense(expense_id) else "Not found.")

        elif choice == "5":
            category = input("Filter by category (leave blank for all): ").strip() or None
            print(f"Total spent: {total_spent(category):.2f}")

        elif choice == "6":
            for month, total in sorted(monthly_summary().items()):
                print(f"{month}: {total:.2f}")

        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    run_cli()


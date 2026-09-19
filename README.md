# Budget Tracker (CRUD + Git/GitHub practice project)

A tiny command-line budget tracker, built to practice two things at
once: Python CRUD operations, and the Git/GitHub workflow.

## What it does

Tracks expenses in a local `expenses.csv` file with four operations:

| CRUD letter | Function             | What it does                       |
|-------------|-----------------------|-------------------------------------|
| Create      | `add_expense()`      | Add a new expense                   |
| Read        | `list_expenses()` / `get_expense()` / `total_spent()` | View expenses and totals |
| Update      | `update_expense()`   | Edit an existing expense            |
| Delete      | `delete_expense()`   | Remove an expense                   |

## Run it

```bash
python budget_tracker.py
```

## Run the tests

```bash
python -m unittest test_budget_tracker.py
```

## Files

- `budget_tracker.py` — the CRUD logic + a simple CLI menu
- `test_budget_tracker.py` — unit tests for the CRUD functions
- `.github/workflows/ci.yml` — GitHub Actions workflow that runs the
  tests automatically on every push and pull request
- `.gitignore` — keeps generated files (like `expenses.csv`) out of Git


"""
test_budget_tracker.py

Basic unit tests for budget_tracker.py.

These run automatically in CI (see .github/workflows/ci.yml) every
time you push to GitHub, so bugs get caught before they reach main.
"""

import os
import unittest
import budget_tracker as bt


class TestBudgetTracker(unittest.TestCase):

    def setUp(self):
        # Use a throwaway file so tests never touch your real data
        bt.DATA_FILE = "test_expenses.csv"
        if os.path.exists(bt.DATA_FILE):
            os.remove(bt.DATA_FILE)

    def tearDown(self):
        if os.path.exists(bt.DATA_FILE):
            os.remove(bt.DATA_FILE)

    def test_add_and_list(self):
        bt.add_expense("2026-09-01", "Food", "Lunch", 15)
        rows = bt.list_expenses()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["category"], "Food")

    def test_total_spent(self):
        bt.add_expense("2026-09-01", "Food", "Lunch", 15)
        bt.add_expense("2026-09-02", "Food", "Dinner", 25)
        self.assertEqual(bt.total_spent("Food"), 40.0)

    def test_update_expense(self):
        eid = bt.add_expense("2026-09-01", "Food", "Lunch", 15)
        bt.update_expense(eid, amount=20)
        self.assertEqual(bt.get_expense(eid)["amount"], "20")

    def test_delete_expense(self):
        eid = bt.add_expense("2026-09-01", "Food", "Lunch", 15)
        self.assertTrue(bt.delete_expense(eid))
        self.assertIsNone(bt.get_expense(eid))


if __name__ == "__main__":
    unittest.main()


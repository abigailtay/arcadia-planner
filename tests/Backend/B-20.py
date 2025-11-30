# File: tests/Backend/B-20.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for adding invalid transactions.
#   Verifies: Invalid (blank, negative) transaction is rejected and not stored.
#   Test Case: B-20 add_transaction: invalid

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.budgetmodel import BudgetModel

def test_add_transaction_invalid():
    budget_model = BudgetModel()
    db_path = "arcadia.db"
    test_cases = [
        {"name": "", "amount": 15.0, "category": "groceries", "type": "expense"},
        {"name": None, "amount": 15.0, "category": "groceries", "type": "expense"},
        {"name": "Negative amount", "amount": -5.0, "category": "bills", "type": "expense"},
        {"name": "No category", "amount": 10.0, "category": "", "type": "income"},
        {"name": "No type", "amount": 10.0, "category": "other", "type": None},
        {"name": "Invalid type", "amount": 10.0, "category": "other", "type": "unknown"},
    ]
    for data in test_cases:
        try:
            transaction_id = budget_model.add_transaction(
                data["name"], data["amount"], data["category"], data["type"]
            )
        except Exception:
            transaction_id = None
        # Confirm with DB lookup: no matching record for invalid insert
        with sqlite3.connect(db_path) as db:
            c = db.cursor()
            c.execute(
                "SELECT transactionId FROM transactions WHERE name=? AND amount=? AND category=? AND type=?",
                (data["name"] or "", data.get("amount", 0), data.get("category") or "", data.get("type") or ""),
            )
            assert c.fetchone() is None

    # Confirm negative amounts are never stored
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT COUNT(*) FROM transactions WHERE amount < 0")
        assert c.fetchone()[0] == 0

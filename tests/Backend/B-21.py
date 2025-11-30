# File: tests/Backend/B-21.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for updating a transaction.
#   Verifies: Only targeted fields updated, others retain current values.
#   Test Case: B-21 update_transaction

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.budgetmodel import BudgetModel

def test_update_transaction():
    budget_model = BudgetModel()
    db_path = "arcadia.db"
    # Initial transaction
    name = "pytest B-21 transaction"
    amount = 100.0
    category = "utilities"
    trans_type = "expense"
    transaction_id = budget_model.add_transaction(name, amount, category, trans_type)

    # Update only the amount and category
    new_amount = 222.22
    new_category = "travel"
    budget_model.update_transaction(transaction_id, amount=new_amount, category=new_category)

    # Fetch from DB and verify changes
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT name, amount, category, type FROM transactions WHERE transactionId=?", (transaction_id,))
        row = c.fetchone()
        assert row is not None
        assert row[0] == name             # Unchanged
        assert abs(row[1] - new_amount) < 0.01   # Updated
        assert row[2] == new_category     # Updated
        assert row[3] == trans_type       # Unchanged

        # Cleanup
        c.execute("DELETE FROM transactions WHERE transactionId=?", (transaction_id,))
        db.commit()

# File: tests/Backend/B-19.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for adding a valid transaction to budget database.
#   Verifies: Adds transaction with valid input, full row in database.
#   Test Case: B-19 add_transaction: valid

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.budgetmodel import BudgetModel

def test_add_transaction_valid():
    budget_model = BudgetModel()
    db_path = "arcadia.db"
    name = "pytest B-19 valid transaction"
    amount = 42.99
    category = "groceries"
    trans_type = "expense"

    # Add transaction
    transaction_id = budget_model.add_transaction(name, amount, category, trans_type)
    assert isinstance(transaction_id, int)

    # Check DB for the full transaction row
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT name, amount, category, type FROM transactions WHERE transactionId=?", (transaction_id,))
        row = c.fetchone()
        assert row is not None
        assert row[0] == name
        assert abs(row[1] - amount) < 0.01
        assert row[2] == category
        assert row[3] == trans_type

        # Cleanup
        c.execute("DELETE FROM transactions WHERE transactionId=?", (transaction_id,))
        db.commit()

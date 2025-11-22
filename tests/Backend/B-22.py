# File: tests/Backend/B-22.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for deleting a transaction.
#   Verifies: Transaction removed from database, no longer available on fetch.
#   Test Case: B-22 delete_transaction

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.budgetmodel import BudgetModel

def test_delete_transaction():
    budget_model = BudgetModel()
    db_path = "arcadia.db"
    name = "pytest B-22 to delete"
    amount = 100.50
    category = "misc"
    trans_type = "expense"

    # Insert transaction to delete
    transaction_id = budget_model.add_transaction(name, amount, category, trans_type)
    assert isinstance(transaction_id, int)

    # Delete the transaction
    ok = budget_model.delete_transaction(transaction_id)
    assert ok is True

    # Try to fetch from DB directly - should not be present
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT * FROM transactions WHERE transactionId=?", (transaction_id,))
        assert c.fetchone() is None

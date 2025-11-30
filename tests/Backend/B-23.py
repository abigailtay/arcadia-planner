# File: tests/Backend/B-23.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for budget analytics.
#   Verifies: Returns accurate sum, average, and filtered results based on data set.
#   Test Case: B-23 analytics_budget

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.budgetmodel import BudgetModel

def test_analytics_budget():
    budget_model = BudgetModel()
    db_path = "arcadia.db"

    # PRE-TEST CLEANUP: Remove pre-existing pytest23 transactions
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM transactions")
        db.commit()
        
    # Insert a batch of test transactions
    test_rows = [
        ("pytest23 grocery",   10.0,  "groceries", "expense"),
        ("pytest23 bus pass",  25.0,  "transport", "expense"),
        ("pytest23 bonus",    100.0,  "income",    "income"),
        ("pytest23 orange",     8.0,  "groceries", "expense"),
        ("pytest23 refund",    10.0,  "groceries", "income"),
    ]
    ids = []
    for row in test_rows:
        ids.append(budget_model.add_transaction(*row))
    try:
        # All transactions, no filter (sum, average, by_category)
        out = budget_model.analytics()
        expected_sum = sum([r[1] for r in test_rows])
        expected_avg = expected_sum / len(test_rows)
        assert abs(out['sum'] - expected_sum) < 0.01
        assert abs(out['average'] - expected_avg) < 0.01
        # Check by_category
        assert out['by_category']['groceries']['sum'] == 10+8+10
        assert out['by_category']['groceries']['count'] == 3
        assert out['by_category']['transport']['sum'] == 25
        assert out['by_category']['income']['sum'] == 100

        # Filter by type=expense
        out_exp = budget_model.analytics(trans_type="expense")
        assert abs(out_exp['sum'] - (10+25+8)) < 0.01
        assert out_exp['by_category']['groceries']['sum'] == 10+8

        # Filter by category=groceries
        out_groc = budget_model.analytics(category="groceries")
        assert abs(out_groc['sum'] - (10+8+10)) < 0.01
        assert out_groc['by_category']['groceries']['count'] == 3

        # Filter by type=income + groceries cat
        out_gi = budget_model.analytics(trans_type="income", category="groceries")
        assert abs(out_gi['sum'] - 10) < 0.01
        assert out_gi['by_category']['groceries']['count'] == 1
    finally:
        # Cleanup
        with sqlite3.connect(db_path) as db:
            c = db.cursor()
            c.execute("DELETE FROM transactions WHERE transactionId IN (%s)" % ",".join("?"*len(ids)), ids)
            db.commit()

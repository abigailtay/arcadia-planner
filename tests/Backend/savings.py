# File: tests/Backend/B-22.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Backend unit tests for savings goals: create, deposit, withdraw, and delete.
#   Assumes new savings_goal methods/tables are present.

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.budgetmodel import BudgetModel

def test_create_and_update_savings_goal():
    budget_model = BudgetModel()
    db_path = "arcadia.db"
    user_id = 1  # use a real user
    name = "pytest goal"
    target_amount = 200.0
    deadline = "2025-12-31"
    notes = "Test goal notes"

    # --- Create goal ---
    goal_id = budget_model.create_savings_goal(user_id, name, target_amount, deadline, notes)
    assert isinstance(goal_id, int)

    # Confirm in DB
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT name, targetAmount, currentAmount, deadline FROM savings_goals WHERE goalId=?", (goal_id,))
        row = c.fetchone()
        assert row is not None
        assert row[0] == name
        assert abs(row[1] - target_amount) < 0.01
        assert abs(row[2]) < 0.01  # starts at zero
        assert row[3] == deadline

    # --- Deposit ---
    new_amt = budget_model.contribute_to_goal(goal_id, user_id, 50.0, 'deposit')
    assert abs(new_amt - 50) < 0.01
    # Confirm change
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT currentAmount FROM savings_goals WHERE goalId=?", (goal_id,))
        amt = c.fetchone()[0]
        assert abs(amt - 50) < 0.01

    # --- Withdraw (valid) ---
    new_amt2 = budget_model.contribute_to_goal(goal_id, user_id, 20.0, 'withdrawal')
    assert abs(new_amt2 - 30) < 0.01
    # Confirm again
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT currentAmount FROM savings_goals WHERE goalId=?", (goal_id,))
        amt = c.fetchone()[0]
        assert abs(amt - 30) < 0.01

    # --- Withdraw too much: should error ---
    with pytest.raises(ValueError):
        budget_model.contribute_to_goal(goal_id, user_id, 100, 'withdrawal')

    # --- List goal transactions ---
    txs = budget_model.list_goal_transactions(goal_id)
    assert isinstance(txs, list)
    assert len(txs) >= 2
    assert set([t['direction'] for t in txs]).issubset({'deposit', 'withdrawal'})

    # --- Delete goal (and cascades transactions) ---
    budget_model.delete_goal(goal_id)
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT * FROM savings_goals WHERE goalId=?", (goal_id,))
        assert c.fetchone() is None
        c.execute("SELECT * FROM savings_transactions WHERE goalId=?", (goal_id,))
        assert c.fetchone() is None

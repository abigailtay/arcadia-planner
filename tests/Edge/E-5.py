"""
File: E-5.py
Author: Allyson Taylor
Date: 2024-06-10
Description:
    Backend unit tests for BudgetModel transaction validation.
    Verifies blank names and invalid/negative transaction values block adds and raise errors.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.budgetmodel import BudgetModel

DB_PATH = 'arcadia.db'

@pytest.fixture
def model():
    return BudgetModel(db_path=DB_PATH)

def test_add_transaction_blank_name(model):
    with pytest.raises(ValueError) as excinfo:
        model.add_transaction(
            name="",
            amount=100,
            category="Groceries",
            trans_type="expense"
        )
    assert "Invalid transaction data" in str(excinfo.value)

def test_add_transaction_none_name(model):
    with pytest.raises(ValueError) as excinfo:
        model.add_transaction(
            name=None,
            amount=50,
            category="Utilities",
            trans_type="expense"
        )
    assert "Invalid transaction data" in str(excinfo.value)

def test_add_transaction_invalid_type(model):
    with pytest.raises(ValueError) as excinfo:
        model.add_transaction(
            name="Gym",
            amount=30,
            category="Health",
            trans_type="spending"  # invalid type
        )
    assert "Invalid transaction data" in str(excinfo.value)

def test_add_transaction_negative_amount(model):
    with pytest.raises(ValueError) as excinfo:
        model.add_transaction(
            name="Salary",
            amount=-500,
            category="Income",
            trans_type="income"
        )
    assert "Invalid transaction data" in str(excinfo.value)

def test_add_transaction_missing_category(model):
    with pytest.raises(ValueError) as excinfo:
        model.add_transaction(
            name="Books",
            amount=30,
            category=None,
            trans_type="expense"
        )
    assert "Invalid transaction data" in str(excinfo.value)

def test_add_transaction_valid(model):
    # Sanity check that valid transaction succeeds and returns ID
    txn_id = model.add_transaction(
        name="Lunch",
        amount=15.75,
        category="Food",
        trans_type="expense"
    )
    assert isinstance(txn_id, int)

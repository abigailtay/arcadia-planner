"""
File: tests/Budget/test_budget_api.py
Author: Allyson Taylor
Date: 2025-11-16
Description:
    Integration tests for Budget backend CRUD and analytics.
    This test generates a log file at tests/budget_api_test_log.txt with all response details (status codes, JSON)
"""

import sys
import os
import pytest
import sqlite3
import logging

# Add project root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from controllers.budget import app

logging.basicConfig(filename='tests/budget_api_test_log.txt', level=logging.INFO, format='%(message)s')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def log_response(resp):
    logging.info(f"Status: {resp.status_code}")
    logging.info(f"Response JSON: {resp.get_json()}")

def test_crud(client):
    # Create transaction (income)
    data = {"name": "Salary", "amount": 5000, "category": "Income", "type": "income"}
    resp = client.post('/transactions', json=data)
    log_response(resp)
    assert resp.status_code == 201
    tid = resp.get_json()["transactionId"]

    # Read transaction
    resp = client.get(f'/transactions/{tid}')
    log_response(resp)
    assert resp.status_code == 200
    assert resp.get_json()["transaction"]["name"] == "Salary"

    # Update transaction amount
    resp = client.put(f'/transactions/{tid}', json={"amount": 5500})
    log_response(resp)
    assert resp.status_code == 200

    # Delete transaction
    resp = client.delete(f'/transactions/{tid}')
    log_response(resp)
    assert resp.status_code == 200

def test_analytics(client):
    # Setup sample transactions for analytics tests
    with sqlite3.connect('arcadia.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM transactions')
        c.executemany(
            'INSERT INTO transactions (name, amount, category, type) VALUES (?, ?, ?, ?)',
            [
                ('Lunch', 12.5, 'Food', 'expense'),
                ('Dinner', 15.0, 'Food', 'expense'),
                ('Bus', 3.0, 'Transport', 'expense'),
                ('Paycheck', 100.0, 'Work', 'income')
            ]
        )
        conn.commit()

    # Test general analytics summary
    resp = client.get('/analytics')
    log_response(resp)
    assert resp.status_code == 200
    data = resp.get_json()["summary"]
    assert "sum" in data
    assert "by_category" in data

    # Test analytics filtered by income type
    resp = client.get('/analytics?type=income')
    log_response(resp)
    assert resp.status_code == 200

    # Test analytics filtered by category Food
    resp = client.get('/analytics?category=Food')
    log_response(resp)
    assert resp.status_code == 200


"""
File: tests/HabitManager/test_habit_api.py
Author: Allyson Taylor
Date: 2025-11-11
Description:
    Unit and integration tests covering habit module API including CRUD operations and streak checks,
    with logging of API responses for screenshot evidence.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from controllers.habitmanager import app
import logging

# Configure logging to file for test evidence
logging.basicConfig(filename='tests/habit_api_test_log.txt', level=logging.INFO, format='%(message)s')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def log_response(resp):
    logging.info(f"Status Code: {resp.status_code}")
    try:
        logging.info(f"JSON Response: {resp.get_json()}")
    except Exception:
        logging.info(f"Response Data: {resp.data}")

def test_create_habit_valid(client):
    payload = {
        'userId': 1,
        'habitName': 'Test Habit',
        'description': 'Testing habit',
        'colorShade': 5,
        'startDate': '2024-01-01'
    }
    resp = client.post('/habits', json=payload)
    log_response(resp)
    assert resp.status_code == 201
    assert resp.json['success']

def test_create_habit_invalid(client):
    payload = {
        'userId': 1,
        'habitName': '',  # Blank habitName invalid
        'colorShade': 20  # invalid
    }
    resp = client.post('/habits', json=payload)
    log_response(resp)
    assert resp.status_code == 400
    assert not resp.json['success']

def test_update_habit(client):
    resp_create = client.post('/habits', json={'userId': 1, 'habitName': 'Update Test'})
    log_response(resp_create)
    h_id = resp_create.json['habitId']
    resp = client.put(f'/habits/{h_id}', json={'habitName': 'Updated Habit Name'})
    log_response(resp)
    assert resp.status_code == 200
    assert resp.json['success']

def test_delete_habit(client):
    resp_create = client.post('/habits', json={'userId': 1, 'habitName': 'Delete Test'})
    log_response(resp_create)
    h_id = resp_create.json['habitId']
    resp = client.delete(f'/habits/{h_id}')
    log_response(resp)
    assert resp.status_code == 200
    assert resp.json['success']

def test_check_in_and_streak(client):
    resp_create = client.post('/habits', json={'userId': 1, 'habitName': 'Check-in Test'})
    log_response(resp_create)
    h_id = resp_create.json['habitId']

    # First check-in today
    resp = client.post(f'/habits/{h_id}/check-in')
    log_response(resp)
    assert resp.status_code == 201
    assert resp.json['success']

    # Attempt second check-in today (should fail)
    resp = client.post(f'/habits/{h_id}/check-in')
    log_response(resp)
    assert resp.status_code == 400

    # Get habit streak
    resp = client.get(f'/habits/{h_id}/streak')
    log_response(resp)
    assert resp.status_code == 200
    assert resp.json['success']
    assert 'streak' in resp.json

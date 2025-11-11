"""
File: tests/TaskManager/test_task_api_regression.py
Author: Allyson Taylor
Date: 2025-11-11
Description:
    Regression tests for Task module verifying all CRUD APIs 
    function correctly after new Habit module additions.
    API responses are logged for verification.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from controllers.taskmanager import app
import logging

logging.basicConfig(filename='tests/task_api_regression_log.txt', level=logging.INFO, format='%(message)s')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def log_response(resp):
    logging.info(f"Status: {resp.status_code}")
    try:
        logging.info(f"JSON: {resp.get_json()}")
    except Exception:
        logging.info(f"Raw data: {resp.data}")

def test_task_crud_full_workflow(client):
    # Create task
    create_resp = client.post('/tasks', json={
        'userId': 1,
        'title': 'Regression Test Task',
        'colorShade': 3,
        'orderIndex': 0
    })
    log_response(create_resp)
    assert create_resp.status_code == 201
    task_id = create_resp.json['taskId']

    # Get tasks
    get_resp = client.get('/tasks?userId=1')
    log_response(get_resp)
    assert get_resp.status_code == 200
    assert any(t['taskId'] == task_id for t in get_resp.json.get('tasks', []))

    # Update task
    update_resp = client.put(f'/tasks/{task_id}', json={'title': 'Updated Regression Task'})
    log_response(update_resp)
    assert update_resp.status_code == 200

    # Reorder tasks
    reorder_resp = client.put('/tasks/reorder', json=[{'taskId': task_id, 'orderIndex': 1}])
    log_response(reorder_resp)
    assert reorder_resp.status_code == 200

    # Delete task
    delete_resp = client.delete(f'/tasks/{task_id}')
    log_response(delete_resp)
    assert delete_resp.status_code == 200

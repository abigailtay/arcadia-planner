# File: tests/Backend/B-12.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for task deletion.
#   Verifies: Task is fully removed from the database.
#   Test Case: B-12 delete_task

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.taskmodel import TaskModel

def test_delete_task():
    task_model = TaskModel()
    db_path = "arcadia.db"
    user_id = 1  # Make sure this user exists
    title = "pytest B-12 Delete Task"
    description = "Task to be deleted by B-12"
    due_date = "2025-12-31"
    category = "testing"
    status = "pending"

    # Create a task
    task_data = {
        "userId": user_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "category": category,
        "status": status
    }
    task_id, err = task_model.create_task(**task_data)
    assert err is None or err == []

    # Delete the task
    task_model.delete_task(task_id)

    # Verify it's gone
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('SELECT * FROM tasks WHERE taskId=?', (task_id,))
        row = c.fetchone()
        assert row is None  # The task should be fully removed

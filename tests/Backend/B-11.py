# File: tests/Backend/B-11.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for partial task update.
#   Verifies: Only provided field(s) are updated in the task record.
#   Test Case: B-11 update_task: partial updates

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.taskmodel import TaskModel

def test_update_task_partial_updates():
    task_model = TaskModel()
    db_path = "arcadia.db"
    user_id = 1  # Must exist
    original_title = "pytest B-11 Original Title"
    original_description = "Original Description"
    new_title = "pytest B-11 New Title"

    # Insert a base task
    insert_data = {
        "userId": user_id,
        "title": original_title,
        "description": original_description,
        "due_date": "2025-12-20",
        "category": "testing",
        "status": "pending"
    }
    task_id, err = task_model.create_task(**insert_data)
    assert err is None or err == []

    # Update only the 'title' field
    errors = task_model.update_task(task_id, title=new_title)
    assert errors is None or errors == []

    # Check DB: title changed, description unchanged
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('SELECT title, description FROM tasks WHERE taskId=?', (task_id,))
        row = c.fetchone()
        assert row is not None
        assert row[0] == new_title
        assert row[1] == original_description

        # Cleanup
        c.execute('DELETE FROM tasks WHERE taskId=?', (task_id,))
        db.commit()

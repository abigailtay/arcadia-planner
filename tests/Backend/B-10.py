# File: tests/Backend/B-10.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for task creation with blank title.
#   Verifies: Blank title results in error, no database row created.
#   Test Case: B-10 create_task: blank title

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.taskmodel import TaskModel

def test_create_task_blank_title():
    task_model = TaskModel()
    db_path = "arcadia.db"
    user_id = 1  # Use an actual valid userId present in your DB
    description = "This task should not be created"
    due_date = "2025-12-31"
    category = "testing"
    status = "pending"

    # Try to insert task with blank title
    task_data = {
        "userId": user_id,
        "title": "",
        "description": description,
        "due_date": due_date,
        "category": category,
        "status": status
    }

    task_id, errors = task_model.create_task(**task_data)

    # Should return an error, or errors list should not be empty
    assert errors and len(errors) > 0

    # Confirm NO task with this description exists in DB
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('SELECT * FROM tasks WHERE description=?', (description,))
        row = c.fetchone()
        assert row is None  # No row should be created

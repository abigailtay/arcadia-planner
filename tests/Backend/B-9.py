# File: tests/Backend/B-9.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for valid task creation.
#   Verifies: Task creation inserts proper record, returns new task ID.
#   Test Case: B-9 create_task: valid input

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.taskmodel import TaskModel

def test_create_task_valid_input():
    task_model = TaskModel()
    db_path = "arcadia.db"
    user_id = 1  # Use an actual valid userId present in your DB
    title = "pytest B-9 Valid Task"
    description = "This is a task created by backend unit test B-9"
    due_date = "2025-12-31"
    category = "testing"
    status = "pending"

    task_data = {
        "userId": user_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "category": category,
        "status": status
    }
    task_id, errors = task_model.create_task(**task_data)
    assert errors is None or errors == []
    assert isinstance(task_id, int)
    
    # Verify in DB directly using sqlite3
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('SELECT title, description, userId FROM tasks WHERE taskId=?', (task_id,))
        row = c.fetchone()
        assert row is not None
        assert row[0] == title
        assert row[1] == description
        assert row[2] == user_id

        # Cleanup
        c.execute('DELETE FROM tasks WHERE taskId=?', (task_id,))
        db.commit()

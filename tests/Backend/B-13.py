# File: tests/Backend/B-13.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for task reordering.
#   Verifies: Tasks reordered by new ID array, orderIndex column matches provided sequence.
#   Test Case: B-13 reorder_tasks

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.taskmodel import TaskModel

def test_reorder_tasks():
    task_model = TaskModel()
    db_path = "arcadia.db"
    user_id = 1  # Use a valid userId

    # Create three test tasks
    task_ids = []
    for i in range(3):
        task_data = {
            "userId": user_id,
            "title": f"B-13 Task {i+1}",
            "description": f"Test task {i+1} for reorder",
            "due_date": "2025-12-20",
            "category": "testing",
            "status": "pending"
        }
        task_id, err = task_model.create_task(**task_data)
        assert err is None or err == []
        task_ids.append(task_id)

    # Define new order (reverse)
    new_order = [{"taskId": tid, "orderIndex": idx} for idx, tid in enumerate(reversed(task_ids))]
    task_model.reorder_tasks(new_order)

    # Verify DB reflects orderIndex changes
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('SELECT taskId, orderIndex FROM tasks WHERE taskId IN (?, ?, ?)', tuple(task_ids))
        results = c.fetchall()
        order_map = {row[0]: row[1] for row in results}
        for idx, tid in enumerate(reversed(task_ids)):
            assert order_map[tid] == idx

        # Cleanup
        c.execute('DELETE FROM tasks WHERE taskId IN (?, ?, ?)', tuple(task_ids))
        db.commit()

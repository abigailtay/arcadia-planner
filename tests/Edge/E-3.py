"""
File: E-3.py
Author: Allyson Taylor
Date: 2024-06-10
Description:
    Backend unit tests for TaskModel create and update validation.
    Verifies blank titles, poorly formatted dates, and invalid edits are blocked with errors.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.taskmodel import TaskModel

DB_PATH = 'arcadia.db'

@pytest.fixture
def model():
    return TaskModel(db_path=DB_PATH)

# You may want an existing test userId. Adjust or query if needed.
TEST_USER_ID = 1

def test_create_task_blank_title(model):
    # Blank title
    task_id, errors = model.create_task(
        userId=TEST_USER_ID,
        title="",
        dueDate="2025-11-25"
    )
    assert errors is not None
    assert 'Title required.' in errors

def test_create_task_bad_due_date(model):
    # Bad date format
    task_id, errors = model.create_task(
        userId=TEST_USER_ID,
        title="Valid title",
        dueDate="not-a-date"
    )
    assert errors is not None
    assert any('Invalid date for dueDate.' in err for err in errors)

def test_create_task_invalid_colorShade(model):
    # Out-of-range color shade
    task_id, errors = model.create_task(
        userId=TEST_USER_ID,
        title="Valid title",
        colorShade=30
    )
    assert errors is not None
    assert any('Color shade invalid.' in err for err in errors)

def test_update_task_blank_title(model):
    # Create valid then try to update title to blank
    task_id, errors = model.create_task(userId=TEST_USER_ID, title="Initial Title")
    assert errors is None
    errors = model.update_task(task_id, title="")
    assert errors is not None
    assert 'Title required.' in errors

def test_update_task_nonsense_due_date(model):
    # Create valid then try to update dueDate to bad date
    task_id, errors = model.create_task(userId=TEST_USER_ID, title="Has a date")
    assert errors is None
    errors = model.update_task(task_id, dueDate="20251199")
    assert errors is not None
    assert any('Invalid date for dueDate.' in err for err in errors)

def test_update_task_invalid_colorShade(model):
    # Create valid then try to edit colorShade
    task_id, errors = model.create_task(userId=TEST_USER_ID, title="Shade test", colorShade=2)
    assert errors is None
    errors = model.update_task(task_id, colorShade="badvalue")
    assert errors is not None
    assert any('Color shade invalid.' in err for err in errors)

"""
File: E-4.py
Author: Allyson Taylor
Date: 2024-06-10
Description:
    Backend tests for HabitModel creation validation.
    Verifies duplicate habit names and invalid color codes are blocked for a user.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.habitmodel import HabitModel

DB_PATH = 'arcadia.db'

@pytest.fixture
def model():
    return HabitModel(db_path=DB_PATH)

TEST_USER_ID = 1

def test_create_habit_valid(model):
    # Should succeed and return a valid habitId
    habit_id = model.create_habit(
        user_id=TEST_USER_ID,
        habit_name="Drink Water",
        color_shade=2
    )
    assert isinstance(habit_id, int)

def test_create_habit_duplicate_name(model):
    habit_name = "DuplicateHabit"
    # First creation should succeed
    habit_id = model.create_habit(
        user_id=TEST_USER_ID,
        habit_name=habit_name,
        color_shade=2
    )
    assert isinstance(habit_id, int)
    # Second creation should raise ValueError for duplicate
    with pytest.raises(ValueError) as excinfo:
        model.create_habit(
            user_id=TEST_USER_ID,
            habit_name=habit_name,
            color_shade=2
        )
    assert "duplicate" in str(excinfo.value).lower()

    assert isinstance(habit_id, int)
    # Second creation should fail
    with pytest.raises(Exception):
        model.create_habit(
            user_id=TEST_USER_ID,
            habit_name=habit_name,
            color_shade=2
        )

def test_create_habit_invalid_color(model):
    with pytest.raises(ValueError) as excinfo:
        model.create_habit(
            user_id=TEST_USER_ID,
            habit_name="ColorTest",
            color_shade=42
        )
    assert "Invalid colorShade" in str(excinfo.value)

def test_create_habit_blank_name(model):
    with pytest.raises(ValueError) as excinfo:
        model.create_habit(
            user_id=TEST_USER_ID,
            habit_name="",
            color_shade=1
        )
    assert "habitName" in str(excinfo.value)

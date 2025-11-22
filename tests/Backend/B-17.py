# File: tests/Backend/B-17.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for duplicate habit check-in in one day.
#   Verifies: Subsequent check-in same day blocked, returns false and no extra DB row.
#   Test Case: B-17 habit_check_in: duplicate check-in

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.habitmodel import HabitModel

def test_habit_check_in_duplicate_same_day():
    habit_model = HabitModel()
    db_path = "arcadia.db"
    user_id = 1  # Make sure user exists
    habit_name = "pytest B-17 Unique Habit"

    # Clean up previous test data
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('DELETE FROM habits WHERE habitName=? AND userId=?', (habit_name, user_id))
        db.commit()
    habit_id = habit_model.create_habit(user_id=user_id, habit_name=habit_name)

    # Clean today's completions
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('DELETE FROM habit_completions WHERE habitId=? AND completionDate=date("now")', (habit_id,))
        db.commit()

    # First check-in should work
    result1 = habit_model.habit_check_in(habit_id)
    assert result1 is True

    # Second check-in same day should be blocked
    result2 = habit_model.habit_check_in(habit_id)
    assert result2 is False

    # Confirm in DB that only one row for today exists
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('SELECT COUNT(*) FROM habit_completions WHERE habitId=? AND completionDate=date("now")', (habit_id,))
        count = c.fetchone()[0]
        assert count == 1

        # Cleanup
        c.execute('DELETE FROM habit_completions WHERE habitId=?', (habit_id,))
        c.execute('DELETE FROM habits WHERE habitId=?', (habit_id,))
        db.commit()

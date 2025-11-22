# File: tests/Backend/B-16.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for daily habit check-in limit.
#   Verifies: Only one check-in recorded per day for each habit.
#   Test Case: B-16 habit_check_in: daily limit

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.habitmodel import HabitModel

def test_habit_check_in_daily_limit():
    habit_model = HabitModel()
    db_path = "arcadia.db"
    user_id = 1  # Must exist
    habit_name = "pytest B-16 habit"

    # Create a habit (cleanup any previous)
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('DELETE FROM habits WHERE habitName=? AND userId=?', (habit_name, user_id))
        db.commit()
    habit_id = habit_model.create_habit(user_id=user_id, habit_name=habit_name)

    # Remove completion for today if present
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('DELETE FROM habit_completions WHERE habitId=? AND completionDate=date("now")', (habit_id,))
        db.commit()

    # First check-in (should succeed)
    first = habit_model.habit_check_in(habit_id)
    assert first is True

    # Second check-in same day (should NOT succeed)
    second = habit_model.habit_check_in(habit_id)
    assert second is False

    # Count rows for today: should be 1
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('SELECT COUNT(*) FROM habit_completions WHERE habitId=? AND completionDate=date("now")', (habit_id,))
        count = c.fetchone()[0]
        assert count == 1

    # Cleanup
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('DELETE FROM habit_completions WHERE habitId=?', (habit_id,))
        c.execute('DELETE FROM habits WHERE habitId=?', (habit_id,))
        db.commit()

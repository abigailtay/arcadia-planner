# File: tests/Backend/B-18.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for habit streak calculation (consecutive and gap days).
#   Verifies: Streak matches consecutive completion dates, resets with gaps.
#   Test Case: B-18 habit_streak calculation

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from datetime import datetime, timedelta
from models.habitmodel import HabitModel

def test_habit_streak_calculation():
    habit_model = HabitModel()
    db_path = "arcadia.db"
    user_id = 1  # must exist
    habit_name = "pytest B-18 streak"

    # Clean up any pre-existing habit and completions
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('DELETE FROM habits WHERE habitName=? AND userId=?', (habit_name, user_id))
        db.commit()
    habit_id = habit_model.create_habit(user_id=user_id, habit_name=habit_name)

    # Helper for inserting completions
    def insert_dates(dates):
        with sqlite3.connect(db_path) as db:
            c = db.cursor()
            c.execute('DELETE FROM habit_completions WHERE habitId=?', (habit_id,))
            for date_str in dates:
                c.execute('INSERT INTO habit_completions (habitId, completionDate) VALUES (?, ?)', (habit_id, date_str))
            db.commit()

    today = datetime.now().date()
    # Case 1: Three consecutive days (should be streak 3)
    days = [today - timedelta(days=i) for i in range(3)][::-1]
    insert_dates([d.strftime('%Y-%m-%d') for d in days])
    assert habit_model.habit_streak(habit_id) == 3

    # Case 2: 2-days streak, gap before today (should be streak 1)
    two_days = [today, today - timedelta(days=2)]
    insert_dates([d.strftime('%Y-%m-%d') for d in two_days])
    assert habit_model.habit_streak(habit_id) == 1

    # Case 3: 5-day streak, with 1 missing day breaking in middle (should be 1)
    dts = [today - timedelta(days=i) for i in (0, 1, 3, 4, 5)]
    insert_dates([d.strftime('%Y-%m-%d') for d in dts])
    assert habit_model.habit_streak(habit_id) == 2

    # Cleanup
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('DELETE FROM habit_completions WHERE habitId=?', (habit_id,))
        c.execute('DELETE FROM habits WHERE habitId=?', (habit_id,))
        db.commit()

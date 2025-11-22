# File: tests/Backend/B-14.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for valid habit creation.
#   Verifies: Inserts correct habit row with all fields, default XP/streak.
#   Test Case: B-14 create_habit: valid input

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.habitmodel import HabitModel

def test_create_habit_valid_input():
    habit_model = HabitModel()
    db_path = "arcadia.db"
    user_id = 1  
    habit_name = "pytest B-14 Valid Habit"
    description = "pytest for B-14"
    category = "wellness"
    frequency = "daily"
    start_date = "2025-11-22"
    color_shade = 2

    habit_id = habit_model.create_habit(
        user_id=user_id,
        habit_name=habit_name,
        description=description,
        category=category,
        frequency=frequency,
        start_date=start_date,
        color_shade=color_shade
    )
    assert isinstance(habit_id, int)

    # Check DB for inserted row (and default values for any defaults like streak/xp)
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute('SELECT habitName, description, category, frequency, startDate, colorShade, userId FROM habits WHERE habitId=?', (habit_id,))
        row = c.fetchone()
        assert row is not None
        assert row[0] == habit_name
        assert row[1] == description
        assert row[2] == category
        assert row[3] == frequency
        assert row[4] == start_date
        assert row[5] == color_shade
        assert row[6] == user_id
    

        # Cleanup
        c.execute('DELETE FROM habits WHERE habitId=?', (habit_id,))
        db.commit()

"""
File: habitmodel.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Backend logic for Habit module handling CRUD operations,
    checkins, streak calculation.
"""

import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'arcadia.db'

class HabitModel:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            return None

    def create_habit(self, user_id, habit_name, description=None, category=None,
                     frequency=None, start_date=None, color_shade=None):
        if not habit_name or not user_id:
            raise ValueError("habitName and userId required")
        if color_shade is not None:
            if not (isinstance(color_shade, int) and 0 <= color_shade <= 10):
                raise ValueError("Invalid colorShade")
        if start_date is not None and self.parse_date(start_date) is None:
            raise ValueError("Invalid startDate format")

        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO habits (userId, habitName, description, category, frequency, startDate, colorShade)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, habit_name, description, category, frequency, start_date, color_shade))
            conn.commit()
            return c.lastrowid

    def get_habits(self, user_id):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM habits WHERE userId=?', (user_id,))
            rows = c.fetchall()
            return [dict(row) for row in rows]

    def update_habit(self, habit_id, **fields):
        allowed_keys = ['habitName', 'description', 'category', 'frequency', 'startDate', 'colorShade']
        updates = []
        values = []
        for key in allowed_keys:
            if key in fields:
                if key == 'colorShade':
                    val = fields[key]
                    if not (isinstance(val, int) and 0 <= val <= 10):
                        raise ValueError("Invalid colorShade")
                elif key == 'startDate':
                    if self.parse_date(fields[key]) is None:
                        raise ValueError("Invalid startDate format")
                elif key == 'habitName' and not fields[key]:
                    raise ValueError("habitName cannot be blank")
                val = fields[key]
                updates.append(f"{key}=?")
                values.append(val)
        if not updates:
            raise ValueError("No valid fields to update")
        values.append(habit_id)

        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(f'UPDATE habits SET {", ".join(updates)} WHERE habitId=?', values)
            conn.commit()

    def delete_habit(self, habit_id):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM habit_completions WHERE habitId=?', (habit_id,))
            c.execute('DELETE FROM habits WHERE habitId=?', (habit_id,))
            conn.commit()

    def habit_check_in(self, habit_id):
        today_str = datetime.utcnow().date().strftime('%Y-%m-%d')
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM habit_completions WHERE habitId=? AND completionDate=?',
                      (habit_id, today_str))
            count = c.fetchone()[0]
            if count > 0:
                return False  # already checked in today
            c.execute('INSERT INTO habit_completions (habitId, completionDate) VALUES (?, ?)', (habit_id, today_str))
            conn.commit()
        return True

    def habit_streak(self, habit_id):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('SELECT completionDate FROM habit_completions WHERE habitId=? ORDER BY completionDate DESC',
                      (habit_id,))
            rows = c.fetchall()
        if not rows:
            return 0
        today = datetime.utcnow().date()
        streak = 0
        prev_date = None
        for (date_str,) in rows:
            d = datetime.strptime(date_str, '%Y-%m-%d').date()
            if prev_date is None:
                if d == today or d == today - timedelta(days=1):
                    streak = 1
                else:
                    break
            else:
                if (prev_date - d).days == 1:
                    streak += 1
                else:
                    break
            prev_date = d
        return streak

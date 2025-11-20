"""
File: taskmodel.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Backend logic for Task Manager.
    Handles CRUD operations, validation, and reordering for tasks.
"""

import sqlite3
from datetime import datetime

DB_PATH = 'arcadia.db'
ALLOWED_COLOR_SHADES = set(range(0, 11))

def valid_date(date_str):
    if not date_str or date_str.strip() == '':
        return True
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

class TaskModel:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def create_task(self, **data):
        errors = []
        if not data.get('title') or data['title'].strip() == '':
            errors.append('Title required.')
        for fld in ['dueDate', 'doDate']:
            if fld in data and not valid_date(data.get(fld)):
                errors.append(f'Invalid date for {fld}.')
        if 'colorShade' in data:
            try:
                color = int(data['colorShade'])
                if color not in ALLOWED_COLOR_SHADES:
                    errors.append('Color shade invalid.')
            except:
                errors.append('Color shade invalid.')
        if errors:
            return None, errors

        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(
                '''INSERT INTO tasks (userId, category, colorShade, title, description, dueDate, doDate, url, orderIndex)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    data['userId'],
                    data.get('category'),
                    data.get('colorShade'),
                    data['title'],
                    data.get('description'),
                    data.get('dueDate'),
                    data.get('doDate'),
                    data.get('url'),
                    data.get('orderIndex')
                )
            )
            task_id = c.lastrowid
            conn.commit()
        return task_id, None

    def get_tasks(self, user_id):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM tasks WHERE userId=? ORDER BY orderIndex ASC', (user_id,))
            rows = c.fetchall()
            return [dict(row) for row in rows]

    def update_task(self, task_id, **data):
        errors = []
        if 'title' in data and (not data['title'] or data['title'].strip() == ''):
            errors.append('Title required.')
        for fld in ['dueDate', 'doDate']:
            if fld in data and not valid_date(data.get(fld)):
                errors.append(f'Invalid date for {fld}.')
        if 'colorShade' in data:
            try:
                color = int(data['colorShade'])
                if color not in ALLOWED_COLOR_SHADES:
                    errors.append('Color shade invalid.')
            except:
                errors.append('Color shade invalid.')
        if errors:
            return errors

        fields = []
        values = []
        for f in ['category','colorShade','title','description','dueDate','doDate','url','orderIndex']:
            if f in data:
                fields.append(f"{f}=?")
                values.append(data[f])
        if not fields:
            return ['No fields to update']
        values.append(task_id)
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('UPDATE tasks SET ' + ', '.join(fields) + ' WHERE taskId=?', values)
            conn.commit()
        return None

    def delete_task(self, task_id):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM tasks WHERE taskId=?', (task_id,))
            conn.commit()

    def reorder_tasks(self, entries):
        with self._get_conn() as conn:
            c = conn.cursor()
            for entry in entries:
                c.execute('UPDATE tasks SET orderIndex=? WHERE taskId=?', (entry['orderIndex'], entry['taskId']))
            conn.commit()

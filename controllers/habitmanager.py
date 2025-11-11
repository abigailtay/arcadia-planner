"""
File: controllers/habitmanager.py
Author: Allyson Taylor
Date: 2025-11-11
Description:
    REST API endpoints for Habit module handling CRUD operations and streak calculation.
"""

from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DB_PATH = 'arcadia.db'


def get_db_connection():
    return sqlite3.connect(DB_PATH, timeout=10)


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None


@app.route('/habits', methods=['POST'])
def create_habit():
    data = request.get_json()
    # Validate mandatory habitName and userId
    if not data.get('habitName') or not data.get('userId'):
        return jsonify({'success': False, 'error': 'habitName and userId required'}), 400
    # Optional: Validate colorShade and startDate formats if provided
    if 'colorShade' in data:
        if not isinstance(data['colorShade'], int) or not (0 <= data['colorShade'] <= 10):
            return jsonify({'success': False, 'error': 'Invalid colorShade'}), 400
    if 'startDate' in data and parse_date(data['startDate']) is None:
        return jsonify({'success': False, 'error': 'Invalid startDate format'}), 400

    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO habits (userId, habitName, description, category, frequency, startDate, colorShade)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (data['userId'], data['habitName'], data.get('description'), data.get('category'),
                   data.get('frequency'), data.get('startDate'), data.get('colorShade')))
        conn.commit()
        habit_id = c.lastrowid
    return jsonify({'success': True, 'habitId': habit_id}), 201


@app.route('/habits', methods=['GET'])
def get_habits():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'success': False, 'error': 'userId required'}), 400
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM habits WHERE userId=?', (user_id,))
        rows = c.fetchall()
        colnames = [col[0] for col in c.description]
        habits = [dict(zip(colnames, row)) for row in rows]
    return jsonify({'success': True, 'habits': habits}), 200


@app.route('/habits/<int:habit_id>', methods=['PUT'])
def update_habit(habit_id):
    data = request.get_json()
    # Validate colorShade and startDate if present
    if 'colorShade' in data:
        if not isinstance(data['colorShade'], int) or not (0 <= data['colorShade'] <= 10):
            return jsonify({'success': False, 'error': 'Invalid colorShade'}), 400
    if 'startDate' in data and parse_date(data['startDate']) is None:
        return jsonify({'success': False, 'error': 'Invalid startDate format'}), 400
    if 'habitName' in data and not data['habitName']:
        return jsonify({'success': False, 'error': 'habitName cannot be blank'}), 400

    fields = []
    values = []
    for key in ['habitName', 'description', 'category', 'frequency', 'startDate', 'colorShade']:
        if key in data:
            fields.append(f"{key}=?")
            values.append(data[key])
    if not fields:
        return jsonify({'success': False, 'error': 'No valid fields to update'}), 400
    values.append(habit_id)

    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute(f'UPDATE habits SET {", ".join(fields)} WHERE habitId=?', values)
        conn.commit()

    return jsonify({'success': True}), 200


@app.route('/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    with get_db_connection() as conn:
        c = conn.cursor()
        # Delete completions first for referential integrity
        c.execute('DELETE FROM habit_completions WHERE habitId=?', (habit_id,))
        c.execute('DELETE FROM habits WHERE habitId=?', (habit_id,))
        conn.commit()
    return jsonify({'success': True}), 200


@app.route('/habits/<int:habit_id>/check-in', methods=['POST'])
def habit_check_in(habit_id):
    today_str = datetime.utcnow().date().strftime('%Y-%m-%d')
    with get_db_connection() as conn:
        c = conn.cursor()
        # Check if already checked in today
        c.execute('SELECT COUNT(*) FROM habit_completions WHERE habitId=? AND completionDate=?', (habit_id, today_str))
        count = c.fetchone()[0]
        if count > 0:
            return jsonify({'success': False, 'error': 'Already checked in today'}), 400
        c.execute('INSERT INTO habit_completions (habitId, completionDate) VALUES (?, ?)', (habit_id, today_str))
        conn.commit()
    return jsonify({'success': True}), 201


@app.route('/habits/<int:habit_id>/streak', methods=['GET'])
def habit_streak(habit_id):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT completionDate FROM habit_completions WHERE habitId=? ORDER BY completionDate DESC', (habit_id,))
        rows = c.fetchall()
    if not rows:
        return jsonify({'success': True, 'streak': 0}), 200
    today = datetime.utcnow().date()
    streak = 0
    prev_date = None
    for (date_str,) in rows:
        d = datetime.strptime(date_str, '%Y-%m-%d').date()
        if prev_date is None:
            # The last completion date has to be today or yesterday to start streak
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
    return jsonify({'success': True, 'streak': streak}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)

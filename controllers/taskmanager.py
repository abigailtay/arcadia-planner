from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'arcadia.db'
ALLOWED_COLOR_SHADES = set(range(0, 11)) # Only 0–10 allowed

def valid_date(date_str):
    if not date_str or date_str.strip() == '':
        return True
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
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
        return jsonify({'success': False, 'errors': errors}), 400
    conn = sqlite3.connect(DB_PATH)
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
    conn.close()
    return jsonify({'success': True, 'taskId': task_id}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'success': False, 'error': 'userId required'}), 400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE userId=? ORDER BY orderIndex ASC', (user_id,))
    rows = c.fetchall()
    colnames = [desc[0] for desc in c.description]
    result = [dict(zip(colnames, row)) for row in rows]
    conn.close()
    return jsonify({'success': True, 'tasks': result}), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
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
        return jsonify({'success': False, 'errors': errors}), 400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fields = []
    values = []
    for f in ['category','colorShade','title','description','dueDate','doDate','url','orderIndex']:
        if f in data:
            fields.append(f"{f}=?")
            values.append(data[f])
    if not fields:
        conn.close()
        return jsonify({'success': False, 'error': 'No fields to update'}), 400
    values.append(task_id)
    c.execute('UPDATE tasks SET ' + ', '.join(fields) + ' WHERE taskId=?', values)
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE taskId=?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

@app.route('/tasks/reorder', methods=['PUT'])
def reorder_tasks():
    data = request.get_json()  # expects list of {taskId, orderIndex}
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for entry in data:
        c.execute('UPDATE tasks SET orderIndex=? WHERE taskId=?', (entry['orderIndex'], entry['taskId']))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

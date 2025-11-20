"""
File: task_controller.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    REST API endpoints for Task Manager.
    Routes call TaskModel for all logic and DB access.
"""

from flask import Flask, request, jsonify
from models.taskmodel import TaskModel

app = Flask(__name__)
task_model = TaskModel()

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_id, errors = task_model.create_task(**data)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    return jsonify({'success': True, 'taskId': task_id}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'success': False, 'error': 'userId required'}), 400
    tasks = task_model.get_tasks(user_id)
    return jsonify({'success': True, 'tasks': tasks}), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    errors = task_model.update_task(task_id, **data)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    return jsonify({'success': True}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task_model.delete_task(task_id)
    return jsonify({'success': True}), 200

@app.route('/tasks/reorder', methods=['PUT'])
def reorder_tasks():
    data = request.get_json()  # expects list of {taskId, orderIndex}
    task_model.reorder_tasks(data)
    return jsonify({'success': True}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

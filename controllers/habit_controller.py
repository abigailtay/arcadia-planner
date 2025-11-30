"""
File: habit_controller.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    REST API endpoints for Habit module.
    Routes call HabitModel for logic and DB access.
"""

from flask import Flask, request, jsonify
from models.habitmodel import HabitModel

app = Flask(__name__)
habit_model = HabitModel()

@app.route('/habits', methods=['POST'])
def create_habit():
    data = request.get_json()
    try:
        habit_id = habit_model.create_habit(
            user_id=data.get('userId'),
            habit_name=data.get('habitName'),
            description=data.get('description'),
            category=data.get('category'),
            frequency=data.get('frequency'),
            start_date=data.get('startDate'),
            color_shade=data.get('colorShade')
        )
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    return jsonify({'success': True, 'habitId': habit_id}), 201

@app.route('/habits', methods=['GET'])
def get_habits():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'success': False, 'error': 'userId required'}), 400
    habits = habit_model.get_habits(user_id)
    return jsonify({'success': True, 'habits': habits}), 200

@app.route('/habits/<int:habit_id>', methods=['PUT'])
def update_habit(habit_id):
    data = request.get_json()
    try:
        habit_model.update_habit(habit_id, **data)
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    return jsonify({'success': True}), 200

@app.route('/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    habit_model.delete_habit(habit_id)
    return jsonify({'success': True}), 200

@app.route('/habits/<int:habit_id>/check-in', methods=['POST'])
def habit_check_in(habit_id):
    success = habit_model.habit_check_in(habit_id)
    if not success:
        return jsonify({'success': False, 'error': 'Already checked in today'}), 400
    return jsonify({'success': True}), 201

@app.route('/habits/<int:habit_id>/streak', methods=['GET'])
def habit_streak(habit_id):
    streak = habit_model.habit_streak(habit_id)
    return jsonify({'success': True, 'streak': streak}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)

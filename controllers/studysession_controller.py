"""
File: studysession_controller.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    REST API endpoints for logging study sessions, querying sessions, 
    and returning study streak, XP, and glitter award details.
    Uses StudySessionModel for DB/storage logic.
"""

from flask import Flask, request, jsonify
from models.studysessionmodel import StudySessionModel
import sqlite3

app = Flask(__name__)
session_model = StudySessionModel()

@app.route('/study/session', methods=['POST'])
def log_study_session():
    data = request.get_json()
    user_id = data.get('userId')
    start_time = data.get('startTime')
    end_time = data.get('endTime')
    setting = data.get('pomodoroSetting')
    if not user_id or not start_time or not end_time or not setting:
        return jsonify({'success': False, 'error': 'Missing parameters'}), 400

    result = session_model.log_session(user_id, start_time, end_time, setting)
    if result:
        return jsonify({'success': True, 'message': 'Session logged.'}), 201
    else:
        return jsonify({'success': False, 'error': 'Session logging failed'}), 400

@app.route('/study/sessions/<int:user_id>', methods=['GET'])
def view_study_sessions(user_id):
    conn = sqlite3.connect("arcadia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM study_sessions WHERE userId=? ORDER BY sessionId DESC", (user_id,))
    colnames = [desc[0] for desc in cursor.description]
    sessions = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'sessions': sessions}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5005)

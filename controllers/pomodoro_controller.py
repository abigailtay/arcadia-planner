"""
File: pomodoro_controller.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    REST API endpoints for Pomodoro session logging and streak calculation,
    calling PomodoroModel for streak logic, XP/glitter rewards, and validation.
"""

from flask import Flask, request, jsonify
from models.pomodoromodel import PomodoroModel
import sqlite3

app = Flask(__name__)
pomodoro_model = PomodoroModel()

@app.route("/pomodoro/session", methods=["POST"])
def create_pomodoro_session():
    data = request.get_json(force=True)
    for field in ("userId", "startTime", "endTime", "pomodoroSetting"):
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    result = pomodoro_model.log_study_session(
        data["userId"],
        data["startTime"],
        data["endTime"],
        data["pomodoroSetting"]
    )

    if result["success"]:
        return jsonify({
            "message": "Session logged.",
            "streak": result.get("streak"),
            "xp": result.get("xp")
        }), 201
    else:
        return jsonify({"error": result["error"]}), 400

@app.route("/pomodoro/streak/<int:user_id>", methods=["GET"])
def get_streak(user_id):
    conn = sqlite3.connect("arcadia.db")
    cur = conn.cursor()
    cur.execute("SELECT streak FROM user WHERE userId=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify({"userId": user_id, "streak": row[0]}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True)

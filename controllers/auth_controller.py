"""
File: auth_controller.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    REST API endpoints for authentication:
    registration, login, token validation, and logout.
    Calls AuthManager model for database and security logic.
"""

from flask import Flask, request, jsonify
from models.authmanager import AuthManager, AuthError

app = Flask(__name__)
auth_manager = AuthManager()

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    username = data.get("username", "")
    password = data.get("password", "")
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    try:
        auth_manager.register_user(username, password)
        return jsonify({"message": f"User {username} registered."}), 201
    except AuthError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = data.get("username", "")
    password = data.get("password", "")
    remember_me = bool(data.get("rememberMe", False))
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    try:
        token = auth_manager.login(username, password, remember_me)
        return jsonify({"token": token}), 200
    except AuthError as e:
        return jsonify({"error": str(e)}), 401

@app.route("/auth/validate", methods=["POST"])
def validate():
    data = request.get_json(force=True)
    token = data.get("token", "")
    if not token:
        return jsonify({"error": "Missing token"}), 400
    try:
        user_id = auth_manager.validate_token(token)
        return jsonify({"userId": user_id}), 200
    except AuthError as e:
        return jsonify({"error": str(e)}), 401

@app.route("/auth/logout", methods=["POST"])
def logout():
    data = request.get_json(force=True)
    token = data.get("token", "")
    if not token:
        return jsonify({"error": "Missing token"}), 400
    try:
        auth_manager.logout(token)
        return jsonify({"message": "Logged out."}), 200
    except AuthError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/auth/request-password-reset", methods=["POST"])
def request_password_reset():
    data = request.get_json(force=True)
    username = data.get("username", "")
    if not username:
        return jsonify({"error": "Missing username"}), 400
    try:
        token = auth_manager.create_password_reset_token(username)
        # In real app, you'd email this token; for demo, return in response.
        return jsonify({"resetToken": token}), 200
    except AuthError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/auth/validate-password-reset", methods=["POST"])
def validate_password_reset():
    data = request.get_json(force=True)
    token = data.get("token", "")
    if not token:
        return jsonify({"error": "Missing token"}), 400
    try:
        user_id = auth_manager.validate_password_reset_token(token)
        return jsonify({"userId": user_id}), 200
    except AuthError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

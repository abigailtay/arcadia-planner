"""
AuthManager for Arcadia Planner
Provides user authentication logic with bcrypt hashing
Author: Allyson Taylor
Last Modified: Nov 5, 2025
"""

import bcrypt
from database.db_manager import DatabaseManager

class AuthManager:
    def __init__(self, db_path='arcadia.db'):
        self.db = DatabaseManager(db_path)
        self.db.connect()

    def hash_password(self, password: str) -> str:
        """Return a bcrypt hash of the plain password."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check_password(self, password: str, stored_hash: str) -> bool:
        """Return True if password matches the stored bcrypt hash."""
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

    def create_user(self, username: str, password: str) -> dict:
        """
        Register a new user with hashed password.
        Fails if the username already exists.
        """
        # Check if username exists
        self.db.cursor.execute(
            "SELECT 1 FROM users WHERE username=?", (username,)
        )
        if self.db.cursor.fetchone():
            return {"success": False, "message": "Username already exists"}
        hashed_pw = self.hash_password(password)
        try:
            self.db.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_pw)
            )
            self.db.connection.commit()
            user_id = self.db.cursor.lastrowid
            return {"success": True, "user_id": user_id, "message": "User created successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def login_user(self, username: str, password: str) -> dict:
        """
        Authenticate user given username and password.
        Returns user_id and username if successful.
        """
        self.db.cursor.execute(
            "SELECT user_id, username, password FROM users WHERE username=?", (username,)
        )
        row = self.db.cursor.fetchone()
        if row and self.check_password(password, row[2]):
            return {
                "success": True,
                "user": {"user_id": row[0], "username": row[1]},
                "message": "Login successful"
            }
        else:
            return {"success": False, "message": "Invalid username or password"}

    def get_user(self, user_id: int) -> dict:
        """
        Retrieve user profile by user_id.
        """
        self.db.cursor.execute(
            "SELECT user_id, username, xp, glitter, streak, last_login FROM users WHERE user_id=?",
            (user_id,)
        )
        row = self.db.cursor.fetchone()
        if row:
            user_dict = {
                "user_id": row[0],
                "username": row[1],
                "xp": row[2],
                "glitter": row[3],
                "streak": row[4],
                "last_login": row[5]
            }
            return {"success": True, "user": user_dict, "message": "User found"}
        else:
            return {"success": False, "message": "User not found"}

    def close(self):
        """Close DB connection."""
        self.db.disconnect()

"""
File: authmanager.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Authentication backend logic for registration, login,
    password verification, and token sessions.
    Handles user and token database management.
"""

import sqlite3
import bcrypt
import secrets
import logging
from datetime import datetime, timedelta

logging.basicConfig(filename='logs/errors.log', level=logging.ERROR)
DB_PATH = 'arcadia.db'

class AuthError(Exception):
    pass

class AuthManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=10)

    def hash_password(self, plain_pw):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_pw.encode(), salt)

    def verify_password(self, plain_pw, hashed_pw):
        try:
            return bcrypt.checkpw(plain_pw.encode(), hashed_pw)
        except Exception:
            return False

    def register_user(self, username, password):
        try:
            with self._get_conn() as conn:
                c = conn.cursor()
                hashed_pw = self.hash_password(password)
                c.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, hashed_pw))
                conn.commit()
        except Exception as e:
            logging.error(f'Registration failed: {e}')
            raise AuthError(f'Registration failed: {e}')

    def login(self, username, password, remember_me=False):
        """
        Returns session token if successful.
        """
        try:
            with self._get_conn() as conn:
                c = conn.cursor()
                c.execute('SELECT userId, password FROM user WHERE username=?', (username,))
                row = c.fetchone()
                if not row:
                    raise AuthError('Invalid credentials.')
                user_id, hashed_pw = row
                if not self.verify_password(password, hashed_pw):
                    raise AuthError('Invalid credentials.')
                token = secrets.token_urlsafe(32)
                expires = datetime.utcnow() + (timedelta(days=14) if remember_me else timedelta(hours=1))
                c.execute('DELETE FROM auth_tokens WHERE user_id=?', (user_id,))
                c.execute('INSERT INTO auth_tokens (token, user_id, expires_at) VALUES (?, ?, ?)',
                          (token, user_id, expires.strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
                return token
        except Exception as e:
            logging.error(f'Login failed: {e}')
            raise AuthError(f'Login failed: {e}')

    def validate_token(self, token):
        try:
            with self._get_conn() as conn:
                c = conn.cursor()
                c.execute('SELECT user_id, expires_at FROM auth_tokens WHERE token=?', (token,))
                row = c.fetchone()
                if not row:
                    raise AuthError('Invalid or expired token.')
                user_id, expires = row
                expires_dt = datetime.strptime(expires, '%Y-%m-%d %H:%M:%S')
                if datetime.utcnow() > expires_dt:
                    c.execute('DELETE FROM auth_tokens WHERE token=?', (token,))
                    conn.commit()
                    raise AuthError('Token expired.')
                return user_id
        except Exception as e:
            logging.error(f'Token validation failed: {e}')
            raise AuthError(f'Token validation failed: {e}')

    def logout(self, token):
        try:
            with self._get_conn() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM auth_tokens WHERE token=?', (token,))
                conn.commit()
        except Exception as e:
            logging.error(f'Logout failed: {e}')
            raise AuthError(f'Logout failed: {e}')
       

    def create_password_reset_token(self, username, expires_in_minutes=60):
        """Generate and store a password reset token for the given user."""
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT userId FROM user WHERE username = ?", (username,))
            row = c.fetchone()
            if not row:
                raise AuthError("User not found.")
            user_id = row[0]
            token = secrets.token_urlsafe(32)
            expires_at = (datetime.utcnow() + timedelta(minutes=expires_in_minutes)).strftime('%Y-%m-%d %H:%M:%S')
            c.execute("""
                INSERT INTO password_reset_tokens (token, user_id, expires_at, used)
                VALUES (?, ?, ?, 0)
            """, (token, user_id, expires_at))
            conn.commit()
            return token

    def validate_password_reset_token(self, token):
        """Check if the reset token is valid, unexpired, and unused. Returns user_id if valid."""
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT user_id, expires_at, used FROM password_reset_tokens WHERE token=?
            """, (token,))
            row = c.fetchone()
            if not row:
                raise AuthError("Invalid reset token.")
            user_id, expires_at, used = row
            if used:
                raise AuthError("Reset token already used.")
            expires_dt = datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S')
            if datetime.utcnow() > expires_dt:
                raise AuthError("Reset token expired.")
            return user_id

    def mark_token_used(self, token):
        """Mark a reset token as used after successful password change."""
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE password_reset_tokens SET used=1 WHERE token=?
            """, (token,))
            conn.commit()


import logging
import bcrypt
import secrets
from datetime import datetime, timedelta
import sqlite3

logging.basicConfig(filename='logs/errors.log', level=logging.ERROR)
DB_PATH = 'arcadia.db'

class AuthError(Exception):
    pass

class AuthManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=10)  # Timeout to wait for locked DB

    def hash_password(self, plain_pw):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_pw.encode(), salt)

    def verify_password(self, plain_pw, hashed_pw):
        try:
            return bcrypt.checkpw(plain_pw.encode(), hashed_pw)
        except Exception:
            return False

    def login(self, username, password, remember_me=False):
        """Returns session token if successful. Optionally issues long-lived token."""
        try:
            with self._get_conn() as conn:
                c = conn.cursor()
                c.execute('SELECT id, password FROM user WHERE username=?', (username,))
                row = c.fetchone()
                if not row:
                    raise AuthError('Invalid credentials.')
                user_id, hashed_pw = row
                if not self.verify_password(password, hashed_pw):
                    raise AuthError('Invalid credentials.')
                token = secrets.token_urlsafe(32)
                expires = datetime.utcnow() + (timedelta(days=14) if remember_me else timedelta(hours=1))
                # Remove any previous tokens for this user (cleanup)
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
                    # Token has expired, cleanup
                    c.execute('DELETE FROM auth_tokens WHERE token=?', (token,))
                    conn.commit()
                    raise AuthError('Token expired.')
                return user_id
        except Exception as e:
            logging.error(f'Token validation failed: {e}')
            raise AuthError(f'Token validation failed: {e}')

    def logout(self, token):
        """Remove session/persistent token from database."""
        try:
            with self._get_conn() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM auth_tokens WHERE token=?', (token,))
                conn.commit()
        except Exception as e:
            logging.error(f'Logout failed: {e}')
            raise AuthError(f'Logout failed: {e}')

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

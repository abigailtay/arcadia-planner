import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from controllers.authmanager import AuthManager
import sqlite3
from datetime import timedelta, datetime

def test_password_hashing():
    auth = AuthManager()
    username = 'test_hash'
    password = 'Secret!992'
    conn = sqlite3.connect('arcadia.db')
    conn.execute('DELETE FROM user WHERE username=?', (username,))
    conn.commit()
    conn.close()
    auth.register_user(username, password)
    conn = sqlite3.connect('arcadia.db')
    cur = conn.execute('SELECT password FROM user WHERE username=?', (username,))
    hashed_pw = cur.fetchone()[0]
    conn.close()
    # Ensure stored password is not the raw password (nor contains it as a substring)
    assert password != hashed_pw  # Most important: not stored as plain text
    if isinstance(hashed_pw, bytes):
        hashed_pw = hashed_pw.decode('utf-8', errors='ignore')
    assert password not in hashed_pw


def test_login_logout():
    auth = AuthManager()
    username = 'test_login'
    password = 'PW!338899'
    conn = sqlite3.connect('arcadia.db')
    conn.execute('DELETE FROM user WHERE username=?', (username,))
    conn.commit()
    conn.close()
    auth.register_user(username, password)
    token = auth.login(username, password, remember_me=False)
    user_id = auth.validate_token(token)
    assert user_id
    auth.logout(token)
    with pytest.raises(Exception):
        auth.validate_token(token)

def test_session_expiry():
    auth = AuthManager()
    username = 'expire_user'
    password = 'ExpireMe!99'
    try:
        auth.register_user(username, password)
    except Exception:
        pass
    # --- Fix: force database unlock before next call ---
    import time, sqlite3
    with sqlite3.connect('arcadia.db') as conn:
        pass  # This will close and unlock any leftover lock
    time.sleep(0.2)  # Tiny sleep can also help for SQLite locks
    token = auth.login(username, password, remember_me=False)
    # Set token expiry
    from datetime import datetime, timedelta
    with sqlite3.connect('arcadia.db') as conn:
        now = datetime.utcnow() - timedelta(seconds=2)
        conn.execute('UPDATE auth_tokens SET expires_at=? WHERE token=?', (now.strftime('%Y-%m-%d %H:%M:%S'), token))
        conn.commit()
    with pytest.raises(Exception):
        auth.validate_token(token)



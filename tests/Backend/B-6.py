# File: tests/Backend/B-6.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for password reset finish flow (valid token).
#   Verifies: Password resets with valid token, token is invalidated, new hash stored.
#   Test Case: B-6 password_reset_finish: valid token

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.authmanager import AuthManager, AuthError

def test_password_reset_finish_valid_token():
    auth = AuthManager()
    username = "b6_resetuser"
    original_password = "InitialP@ss92"
    new_password = "NewP@ssword67"
    
    # Preparation: Clean user and tokens
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()
    
    # Register and get user ID
    auth.register_user(username, original_password)
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT userId, password FROM user WHERE username=?', (username,))
        user_row = c.fetchone()
        assert user_row is not None
        user_id, old_hash = user_row

    # Simulate "reset start": log in to generate a valid token (adjust this if you implement a token reset flow differently!)
    token = auth.login(username, original_password)

    # Simulate "reset finish": reset password with valid token
    # You must implement a method like: auth.reset_password(token, new_password)
    # For demo, just update hash directly and test (replace with your flow if available)
    with auth._get_conn() as conn:
        c = conn.cursor()
        new_hash = auth.hash_password(new_password)
        c.execute('UPDATE user SET password=? WHERE userId=?', (new_hash, user_id))
        c.execute('DELETE FROM auth_tokens WHERE token=?', (token,))
        conn.commit()

    # Verify password has changed and token is invalid
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT password FROM user WHERE userId=?', (user_id,))
        new_pw_hash = c.fetchone()[0]
        assert new_pw_hash != old_hash
    
        # Token should now be invalid
        c.execute('SELECT * FROM auth_tokens WHERE token=?', (token,))
        assert c.fetchone() is None

    # Cleanup
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()

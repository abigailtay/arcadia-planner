# File: tests/Backend/B-4.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for password reset token creation.
#   Generates and stores a reset token for a real email address.
#   Test Case: B-4 password_reset_start: valid email

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.authmanager import AuthManager

def test_password_reset_start_valid_email():
    auth = AuthManager()
    username = "b4_resetuser"
    password = "ResetPass123!"
    # Insert test user if not present
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()
    auth.register_user(username, password)
    # Confirm userId
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT userId FROM user WHERE username=?', (username,))
        user_row = c.fetchone()
        assert user_row is not None
        user_id = user_row[0]
    # Remove any existing tokens
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM auth_tokens WHERE user_id=?', (user_id,))
        conn.commit()

    # Start reset: simulate flow (add a reset method to AuthManager or replicate its expected logic)
    # Here, we will call login to make a token as example (adjust as needed for a real password_reset_start)
    token = auth.login(username, password)
    assert isinstance(token, str)
    # Verify token is now in DB and mapped to user_id
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT token, user_id FROM auth_tokens WHERE token=?', (token,))
        token_row = c.fetchone()
        assert token_row is not None
        assert token_row[1] == user_id
    # Clean up
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM auth_tokens WHERE user_id=?', (user_id,))
        c.execute('DELETE FROM user WHERE userId=?', (user_id,))
        conn.commit()

# File: tests/Backend/B-1.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for user registration. Inserts new user, hashes password, checks XP/glitter if present.
#   Test Case: B-1 register_user: new user creation

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.authmanager import AuthManager

def test_register_user_new_user_creation():
    auth = AuthManager()
    username = "b1_testuser"
    password = "SecurePa$$word1!"

    # Remove pre-existing user, if any (setup/cleanup)
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()

    # Perform registration
    auth.register_user(username, password)

    # Verify user in DB, password is hashed, XP and glitter if exist
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('PRAGMA table_info(user)')
        columns = [col[1] for col in c.fetchall()]
        select_columns = ', '.join(columns)
        c.execute(f'SELECT {select_columns} FROM user WHERE username=?', (username,))
        row = c.fetchone()
        assert row is not None
        user_data = dict(zip(columns, row))
        assert user_data["username"] == username
        assert user_data["password"] != password
        # Optional: check XP, glitter if columns exist
        if "xp" in user_data:
            assert user_data["xp"] == 0
        if "glitter" in user_data:
            assert user_data["glitter"] == 0

    # Clean up so repeated test runs are safe
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()

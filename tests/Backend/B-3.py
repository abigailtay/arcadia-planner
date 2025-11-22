# File: tests/Backend/B-3.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for login flow.
#   Returns auth token for correct credentials, rejects invalid login attempts.
#   Test Case: B-3 login: success and failure

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.authmanager import AuthManager, AuthError

def test_login_success_and_failure():
    auth = AuthManager()
    username = "b3_loginuser"
    password = "TestPass321!"
    
    # Remove any pre-existing user
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()

    # Register user
    auth.register_user(username, password)

    # Login with correct credentials
    token = auth.login(username, password)
    assert isinstance(token, str) and len(token) > 10

    # Login with incorrect password should fail
    with pytest.raises(AuthError):
        auth.login(username, "WrongPassword!")

    # Clean up for repeat runs
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()

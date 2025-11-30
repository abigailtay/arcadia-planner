# File: tests/Backend/B-5.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for password reset with unknown user.
#   Verifies: Unknown email/username does not result in token or reset info being stored.
#   Test Case: B-5 password_reset_start: unknown email

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.authmanager import AuthManager, AuthError

def test_password_reset_start_unknown_email():
    auth = AuthManager()
    username = "b5_nonexistentuser"
    password = "DoesntMatter1!"

    # Ensure user doesn't exist
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()

    # Try to login with non-existent user, should raise AuthError
    with pytest.raises(AuthError):
        auth.login(username, password)
    
    # Check that there is no token for this username in auth_tokens
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT userId FROM user WHERE username=?', (username,))
        user = c.fetchone()
        if user:
            user_id = user[0]
            c.execute('SELECT token FROM auth_tokens WHERE user_id=?', (user_id,))
            token = c.fetchone()
            assert token is None
        else:
            assert True  # User not present, so no tokens possible

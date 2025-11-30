# File: tests/Backend/B-2.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for duplicate username registration. Should raise AuthError and not create new row.
#   Test Case: B-2 register_user: duplicate username

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.authmanager import AuthManager, AuthError

def test_register_user_duplicate_username():
    auth = AuthManager()
    username = "b2_dupeuser"
    password = "DupePass123!"
    
    # Remove user if exists
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()
    
    # Register user first time (should succeed)
    auth.register_user(username, password)
    
    # Try duplicate registration, should raise AuthError
    with pytest.raises(AuthError):
        auth.register_user(username, password)
    
    # Ensure only one user row exists
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM user WHERE username=?', (username,))
        count = c.fetchone()[0]
        assert count == 1
    
    # Clean up so repeat runs work
    with auth._get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM user WHERE username=?', (username,))
        conn.commit()

"""
File: E-2.py
Author: Allyson Taylor
Date: 2024-06-10
Description:
    Backend test for AuthManager password reset token validation.
    Verifies expired, used, or invalid tokens are correctly rejected.
"""

import sys
import os

# Always add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.authmanager import AuthManager, AuthError

DB_PATH = 'arcadia.db'

@pytest.fixture
def manager():
    return AuthManager(db_path=DB_PATH)

@pytest.fixture
def username(manager):
    # Make sure test user exists
    uname = "reset_edge_user"
    try:
        manager.register_user(uname, "OriginalPassword1!")
    except AuthError:
        pass
    return uname

def test_expired_token(manager, username):
    # Create token that is already expired (expires in -1 min)
    token = manager.create_password_reset_token(username, expires_in_minutes=-1)
    with pytest.raises(AuthError):
        manager.validate_password_reset_token(token)

def test_used_token(manager, username):
    token = manager.create_password_reset_token(username, expires_in_minutes=10)
    manager.mark_token_used(token)
    with pytest.raises(AuthError):
        manager.validate_password_reset_token(token)

def test_invalid_token(manager):
    with pytest.raises(AuthError):
        manager.validate_password_reset_token("notarealtoken123")

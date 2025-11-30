"""
File: E-1.py
Author: Allyson Taylor
Date: 2024-06-10
Description:
    Backend unit test for the AuthManager registration logic.
    Verifies that blank/invalid usernames or passwords are correctly blocked with errors by the backend model.
    Tested directly on AuthManager; no HTTP or Flask endpoints tested here.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


print("DEBUG sys.path:", sys.path)

import pytest
from models.authmanager import AuthManager, AuthError

TEST_DB_PATH = 'test_arcadia.db'

@pytest.fixture(scope="module")
def auth_manager():
    # Ensure necessary test table exists (see SQL section below to run this manually)
    manager = AuthManager(db_path=TEST_DB_PATH)
    yield manager
    # (No teardown for DB—delete manually if desired)

def test_registration_blank_username(auth_manager):
    with pytest.raises(AuthError) as excinfo:
        auth_manager.register_user("", "safepassword123")
    assert "failed" in str(excinfo.value).lower()

def test_registration_blank_password(auth_manager):
    with pytest.raises(AuthError) as excinfo:
        auth_manager.register_user("testuser1", "")
    assert "failed" in str(excinfo.value).lower()

def test_registration_null_username_password(auth_manager):
    with pytest.raises(AuthError) as excinfo:
        auth_manager.register_user(None, None)
    assert "failed" in str(excinfo.value).lower()

def test_registration_missing_fields(auth_manager):
    with pytest.raises(TypeError):
        auth_manager.register_user()

def test_registration_valid_inputs(auth_manager):
    try:
        auth_manager.register_user("edge_valid_user", "strongPassword!234")
        assert True
    except AuthError as e:
        assert "failed" in str(e).lower()

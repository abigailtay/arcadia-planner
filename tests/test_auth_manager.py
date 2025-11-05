import pytest
from src.controllers.auth_manager import AuthManager
import os
from database.db_manager import DatabaseManager

test_db = "test_arcadia.db"

def setup_module(module):
    if os.path.exists(test_db):
        os.remove(test_db)
    db = DatabaseManager(db_path=test_db)
    db.connect()
    db.create_tables()
    db.disconnect()

def teardown_module(module):
    if os.path.exists(test_db):
        os.remove(test_db)

def test_create_and_login_user():
    auth = AuthManager(db_path=test_db)
    username = "testuser"
    password = "SafePass123!"
    # Create user
    result = auth.create_user(username, password)
    assert result["success"]
    # Correct login
    login = auth.login_user(username, password)
    assert login["success"]
    # Wrong password
    bad_login = auth.login_user(username, "badpass")
    assert not bad_login["success"]
    auth.close()

def test_duplicate_user():
    auth = AuthManager(db_path=test_db)
    username = "repeat"
    password = "Password!1"
    result1 = auth.create_user(username, password)
    result2 = auth.create_user(username, password)
    assert result1["success"]
    assert not result2["success"]  # Duplicate user should fail
    auth.close()

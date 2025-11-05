import pytest
from src.controllers.auth_manager import AuthManager
import os
from database.db_manager import DatabaseManager

test_db = "test_arcadia.db"

def setup_module(module):
    if os.path.exists(test_db):
        os.remove(test_db)
    db = DatabaseManager(test_db)
    db.connect()
    db.create_tables()
    db.disconnect()

def teardown_module(module):
    if os.path.exists(test_db):
        os.remove(test_db)

def test_create_user():
    auth = AuthManager(db_path=test_db)
    result = auth.create_user("userA", "SecretPass#1")
    assert result["success"] is True
    auth.close()

def test_duplicate_user():
    auth = AuthManager(db_path=test_db)
    auth.create_user("duplicate", "SecretPass#2")
    again = auth.create_user("duplicate", "Other#2")
    assert again["success"] is False
    auth.close()

def test_login_user():
    auth = AuthManager(db_path=test_db)
    auth.create_user("loginname", "LogPass992!")
    good = auth.login_user("loginname", "LogPass992!")
    bad = auth.login_user("loginname", "wrong!")
    assert good["success"] is True
    assert bad["success"] is False
    auth.close()

def test_get_user():
    auth = AuthManager(db_path=test_db)
    new = auth.create_user("fetch", "Pass1Key!")
    uid = new.get("user_id")
    found = auth.get_user(uid)
    assert found["success"] is True
    assert found["user"]["username"] == "fetch"
    auth.close()


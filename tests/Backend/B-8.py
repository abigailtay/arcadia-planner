# File: tests/Backend/B-8.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for password hashing and verification.
#   Verifies: Passwords are stored only as hashes, verify logic works for valid/invalid password.
#   Test Case: B-8 hash_password and verify

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.authmanager import AuthManager

def test_hash_password_and_verify():
    auth = AuthManager()
    password = "SomeC00lPassword$"
    wrong_password = "badPassword123"
    # Hash the password
    hashed = auth.hash_password(password)
    assert hashed != password
    assert isinstance(hashed, bytes)
    # Correct password should verify
    assert auth.verify_password(password, hashed) is True
    # Incorrect password should not verify
    assert auth.verify_password(wrong_password, hashed) is False

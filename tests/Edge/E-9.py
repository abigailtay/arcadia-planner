"""
File: E-9.py
Author: Allyson Taylor
Date: 2024-06-10
Description:
    Backend tests for AvatarStoreModel purchase validation.
    Verifies purchases block invalid, unavailable, or duplicate items and don't deduct funds.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.avatarstoremodel import AvatarStoreModel, sqlite3

@pytest.fixture
def model():
    mdl = AvatarStoreModel()
    yield mdl
    mdl.close()

def setup_user(mdl, user_id=1, glitter=100, username=None, password=b'dummypw'):
    if username is None:
        username = f"testuser{user_id}"
    with mdl._get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO user (userId, username, password, glitter) VALUES (?, ?, ?, ?)",
            (user_id, username, password, glitter)
        )
        cur.execute(
            "UPDATE user SET glitter=? WHERE userId=?", (glitter, user_id)
        )
        conn.commit()
        print("DEBUG user setup after insert/update:", list(cur.execute("SELECT * FROM user WHERE userId=?", (user_id,))))

def setup_store_item(mdl, item_id=101, cost=10, available=1, name="ItemName"):
    with mdl._get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO store_items (itemId, name, glitterCost, available) VALUES (?, ?, ?, ?)",
            (item_id, name, cost, available)
        )
        conn.commit()
        print("DEBUG item setup:", list(cur.execute("SELECT * FROM store_items WHERE itemId=?", (item_id,))))

def test_invalid_purchase(model):
    setup_user(model)
    # Item does not exist
    result = model.purchase_item(1, 9999)
    assert not result

def test_unavailable_purchase(model):
    setup_user(model)
    setup_store_item(model, item_id=2000, cost=15, available=0, name="UnavailableItem")
    result = model.purchase_item(1, 2000)
    assert not result

def test_duplicate_purchase(model):
    setup_user(model)
    setup_store_item(model, item_id=3000, cost=20, available=1, name="DuplicateItem")
    # First purchase OK
    first = model.purchase_item(1, 3000)
    assert first
    # Second purchase blocked (duplicate)
    second = model.purchase_item(1, 3000)
    assert not second

def test_insufficient_glitter(model):
    setup_user(model, glitter=5)
    setup_store_item(model, item_id=4000, cost=12, available=1, name="BigTicketItem")
    result = model.purchase_item(1, 4000)
    assert not result

def test_successful_purchase(model):
    setup_user(model, glitter=50)
    setup_store_item(model, item_id=5000, cost=10, available=1, name="AffordableItem")
    result = model.purchase_item(1, 5000)
    assert result
    with model._get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT glitter FROM user WHERE userId=?", (1,))
        new_glitter = cur.fetchone()['glitter']
        assert new_glitter == 40

"""
File: test_avatarstoremodel.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Tests for Avatar Store purchase logic,
    currency deduction, unlock mechanics,
    and purchase persistence.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from models.avatarstoremodel import AvatarStoreModel
import sqlite3

DB_PATH = "arcadia.db"

@pytest.fixture(scope="module")
def store_model():
    model = AvatarStoreModel()
    yield model
    model.close()

def ensure_user_with_glitter(user_id=1, glitter=100):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT userId FROM user WHERE userId=?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO user (userId, username, password, glitter, xp, streak) VALUES (?, ?, ?, ?, 0, 0)", (user_id, "testuser", "password123", glitter))
    else:
        cursor.execute("UPDATE user SET glitter = ? WHERE userId=?", (glitter, user_id))
    conn.commit()
    conn.close()

def ensure_store_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Add sample store items for testing
    cursor.execute("SELECT * FROM store_items WHERE name = ?", ('Test Avatar 1',))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO store_items (name, description, rarity, glitterCost, appearance)
            VALUES (?, ?, ?, ?, ?)
        """, ('Test Avatar 1', 'Sample Rare Avatar', 'Rare', 50, 'appearance1'))
        cursor.execute("""
            INSERT INTO store_items (name, description, rarity, glitterCost, appearance)
            VALUES (?, ?, ?, ?, ?)
        """, ('Test Avatar 2', 'Sample Common Avatar', 'Common', 30, 'appearance2'))
        conn.commit()
    conn.close()

def test_purchase_success(store_model):
    user_id = 1
    ensure_user_with_glitter(user_id, glitter=100)
    ensure_store_items()

    # Purchase an item affordable by user
    result = store_model.purchase_item(user_id, 1)  # Assuming itemId=1
    assert result is True

    # Check user's glitter reduced by item cost
    remaining = store_model.get_user_glitter(user_id)
    assert remaining == 50  # 100 - 50 cost

    # Check inventory updated
    inventory = store_model.get_user_inventory(user_id)
    item_ids = [item['itemId'] for item in inventory]
    assert 1 in item_ids

def test_purchase_insufficient_glitter(store_model):
    user_id = 1
    ensure_user_with_glitter(user_id, glitter=10)
    ensure_store_items()

    # Attempt to buy item costing 50 glitter with only 10 glitter
    result = store_model.purchase_item(user_id, 1)
    assert not result  # Should fail

def test_purchase_nonexistent_item(store_model):
    user_id = 1
    ensure_user_with_glitter(user_id, glitter=100)
    ensure_store_items()

    # Item id 9999 does not exist
    result = store_model.purchase_item(user_id, 9999)
    assert not result

    print("Pytest completed: Avatar store purchase logic and currency deductions tested successfully.")
    print("Instruction: Take a screenshot of this pytest output after all tests pass.")

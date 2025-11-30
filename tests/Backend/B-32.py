# File: tests/Backend/B-32.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Unit test for purchasing a store item (once only), and database updates.
#   Verifies: Can buy item once, duplicate is rejected, glitter and inventory update correctly.
#   Test Case: B-32 store_purchase_item

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sqlite3
from models.avatarstoremodel import AvatarStoreModel

def test_store_purchase_item():
    db_path = "arcadia.db"
    test_user_id = 73737
    test_username = "pytestbuyer"
    test_password = "pw"
    test_item_name = "pytest store boots"
    test_item_cost = 99
    test_item_id = None

    # Cleanup before: remove any test user, inventory, and test item
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        # Remove test item & inventory first (to get itemId cleanly for current run)
        c.execute("DELETE FROM store_items WHERE name=?", (test_item_name,))
        c.execute("DELETE FROM user_inventory WHERE userId=?", (test_user_id,))
        c.execute("DELETE FROM user WHERE userId=?", (test_user_id,))
        db.commit()

    # Add a store item
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute(
            "INSERT INTO store_items (name, description, rarity, glitterCost, appearance) VALUES (?, ?, ?, ?, ?)",
            (test_item_name, "Boots for pytest B-32", "uncommon", test_item_cost, "boots.png")
        )
        test_item_id = c.lastrowid
        db.commit()

    # Add a user with enough glitter
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("INSERT INTO user (userId, username, password, xp, glitter) VALUES (?, ?, ?, 0, ?)",
                  (test_user_id, test_username, test_password, test_item_cost + 50))
        db.commit()

    store_model = AvatarStoreModel()

    try:
        # Before purchase: user glitter and inventory
        before_glitter = store_model.get_user_glitter(test_user_id)
        assert before_glitter >= test_item_cost

        # Buy once: should succeed, deduct glitter, add to inventory
        success = store_model.purchase_item(test_user_id, test_item_id)
        assert success, "First purchase failed"
        after_glitter = store_model.get_user_glitter(test_user_id)
        assert after_glitter == before_glitter - test_item_cost

        # Check inventory
        inventory = store_model.get_user_inventory(test_user_id)
        item_ids = [item["itemId"] if isinstance(item, dict) else item[0] for item in inventory]
        assert test_item_id in item_ids, "Test item not found in user inventory after purchase!"

        # Try buying a second time -- should reject (you may need to ensure DB-level unique constraint or logic)
        second_attempt = store_model.purchase_item(test_user_id, test_item_id)
        assert not second_attempt, "Duplicate purchase was not rejected"

    finally:
        # Clean up user, item, inventory for DB hygiene
        with sqlite3.connect(db_path) as db:
            c = db.cursor()
            c.execute("DELETE FROM user_inventory WHERE userId=?", (test_user_id,))
            c.execute("DELETE FROM user WHERE userId=?", (test_user_id,))
            c.execute("DELETE FROM store_items WHERE itemId=?", (test_item_id,))
            db.commit()
        store_model.close()

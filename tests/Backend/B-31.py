# File: tests/Backend/B-31.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Unit test for store item listing (no avatar items present).
#   Inserts a test item and ensures correct DB cleanup.
#   Verifies: Lists all store items from DB, no avatar items present.
#   Test Case: B-31 store_get_items

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sqlite3
import pytest

def test_store_get_items_no_avatars():
    db_path = "arcadia.db"
    test_name = "pytest store hat"
    test_item_id = None  # We'll grab the rowid after insert

    # Insert a sample non-avatar store item before test
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute(
            "INSERT INTO store_items (name, description, rarity, glitterCost, appearance) VALUES (?, ?, ?, ?, ?)",
            (test_name, "A hat for pytest B-31", "common", 25, "hat_image.png")
        )
        test_item_id = c.lastrowid
        db.commit()

    try:
        with sqlite3.connect(db_path) as db:
            c = db.cursor()
            c.execute("SELECT * FROM store_items")
            rows = c.fetchall()
            colnames = [d[0] for d in c.description]
            store_items = [dict(zip(colnames, row)) for row in rows]
        
        # No item should have 'avatar' in name, description, or appearance
        for item in store_items:
            for field in ["name", "description", "appearance"]:
                value = str(item.get(field, "")).lower()
                assert "avatar" not in value, f"Avatar item wrongly in store: {item}"

        # Our test item should be present
        assert any(item["name"] == test_name for item in store_items), "Test item not found in store items."

        print(f"Store items checked. Test item present; no avatar items found.")
    finally:
        # Cleanup - remove the test store item
        with sqlite3.connect(db_path) as db:
            c = db.cursor()
            c.execute("DELETE FROM store_items WHERE name=?", (test_name,))
            db.commit()

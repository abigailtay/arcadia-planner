# File: tests/Backend/B-26.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for adding stickers to recipe box.
#   Verifies: Only valid stickers added to DB; bad data blocked with error.
#   Test Case: B-26 add_sticker

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.recipeboxmodel import RecipeBoxModel

def test_add_sticker():
    recipe_model = RecipeBoxModel()
    db_path = 'arcadia.db'
    test_name = "pytest-sticker"
    test_url = "https://example.com/image.jpg"

    # Clean any existing with this name before/after test
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM stickers WHERE name=?", (test_name,))
        db.commit()

    # Add a valid sticker
    sticker_id = recipe_model.add_sticker(test_name, test_url)
    assert isinstance(sticker_id, int)
    # Confirm in DB
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT name, imageURL FROM stickers WHERE stickerId=?", (sticker_id,))
        row = c.fetchone()
        assert row is not None
        assert row[0] == test_name
        assert row[1] == test_url

    # Try invalid stickers (missing one or both fields)
    bad_cases = [
        (None, test_url),
        ("", test_url),
        (test_name, ""),
        (test_name, None),
        (None, None),
        ("", ""),
    ]
    for name, url in bad_cases:
        with pytest.raises(ValueError):
            recipe_model.add_sticker(name, url)

    # Cleanup
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM stickers WHERE name=?", (test_name,))
        db.commit()

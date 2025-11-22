# File: tests/Backend/B-27.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for attaching/detaching stickers to recipes.
#   Verifies: Sticker properly assigned and can be detached from recipe in DB.
#   Test Case: B-27 attach_sticker

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.recipeboxmodel import RecipeBoxModel

def test_attach_sticker():
    recipe_model = RecipeBoxModel()
    db_path = 'arcadia.db'

    # Clean up
    test_title = "pytest B-27 recipe"
    test_sticker_name = "pytest-sticker-B27"
    test_sticker_url = "https://example.com/imgB27.jpg"
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM recipes WHERE title=?", (test_title,))
        c.execute("DELETE FROM stickers WHERE name=?", (test_sticker_name,))
        db.commit()

    # Add sticker and recipe (no sticker initially)
    sticker_id = recipe_model.add_sticker(test_sticker_name, test_sticker_url)
    recipe_id = recipe_model.add_recipe(title=test_title, instructions="Attach sticker test")

    # Attach sticker
    recipe_model.update_recipe(recipe_id, stickerId=sticker_id)
    rec = recipe_model.get_recipe(recipe_id)
    assert rec["stickerId"] == sticker_id

    # Detach (set to None)
    recipe_model.update_recipe(recipe_id, stickerId=None)
    rec2 = recipe_model.get_recipe(recipe_id)
    assert rec2["stickerId"] is None

    # Cleanup
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM recipes WHERE title=?", (test_title,))
        c.execute("DELETE FROM stickers WHERE name=?", (test_sticker_name,))
        db.commit()

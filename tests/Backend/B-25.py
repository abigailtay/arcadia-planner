# File: tests/Backend/B-25.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for invalid or malformed recipe measurements.
#   Verifies: Invalid or malformed measures block recipe creation and show error.
#   Test Case: B-25 add_recipe: invalid measure

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.recipeboxmodel import RecipeBoxModel

def test_add_recipe_invalid_measure():
    recipe_model = RecipeBoxModel()
    db_path = 'arcadia.db'
    test_title = "pytest B-25 invalid measure"

    # Clean up before/after
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM recipes WHERE title=?", (test_title,))
        db.commit()

    # None is valid (means no measurement); others should error
    bad_values = ["not_a_number", "1/0", "2..5", "!!", "0/0", ""]
    for bad_value in bad_values:
        with pytest.raises(ValueError):
            recipe_model.add_recipe(
                title=test_title,
                instructions="Will not save.",
                measurement=bad_value
            )

    # Confirm that no recipe with this title is present
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT * FROM recipes WHERE title=?", (test_title,))
        assert c.fetchone() is None

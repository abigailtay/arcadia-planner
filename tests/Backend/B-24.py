# File: tests/Backend/B-24.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for adding valid recipes with fractional/decimal measures.
#   Verifies: Inserts valid recipe; measures parsed and returned as fraction if applicable.
#   Test Case: B-24 add_recipe: valid

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from models.recipeboxmodel import RecipeBoxModel

def test_add_recipe_valid():
    recipe_model = RecipeBoxModel()
    db_path = 'arcadia.db'
    # Clean up any test recipes before/after
    test_title = "pytest B-24 banana bread"
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM recipes WHERE title=?", (test_title,))
        db.commit()

    # Add with fraction string measurement
    recipe_id_1 = recipe_model.add_recipe(
        title=test_title,
        instructions="Mix and bake.",
        measurement="3/4"
    )
    assert isinstance(recipe_id_1, int)
    rec_1 = recipe_model.get_recipe(recipe_id_1)
    assert rec_1 is not None
    assert rec_1['title'] == test_title
    assert rec_1['measurement'] == "3/4"

    # Add with decimal measurement
    recipe_id_2 = recipe_model.add_recipe(
        title=test_title,
        instructions="Mix and bake.",
        measurement=0.5
    )
    rec_2 = recipe_model.get_recipe(recipe_id_2)
    assert rec_2['measurement'] == "1/2"

    # Add with integer measurement
    recipe_id_3 = recipe_model.add_recipe(
        title=test_title,
        instructions="Stir.",
        measurement=2
    )
    rec_3 = recipe_model.get_recipe(recipe_id_3)
    assert rec_3['measurement'] == "2"

    # Cleanup
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM recipes WHERE title=?", (test_title,))
        db.commit()

"""
File: E-6.py
Author: Allyson Taylor
Date: 2025-11-22
Description:
    Backend tests for RecipeBoxModel creation/update validation.
    Verifies that invalid measurement, blank title, or sticker data blocks creation with proper errors.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.recipeboxmodel import RecipeBoxModel

DB_PATH = 'arcadia.db'

@pytest.fixture
def model():
    return RecipeBoxModel(db_path=DB_PATH)

def test_add_recipe_blank_title(model):
    # Should raise error if title is blank
    with pytest.raises(Exception):
        model.add_recipe(
            title="",
            instructions="Mix ingredients",
            measurement="1/2"
        )

def test_add_recipe_invalid_measurement(model):
    # Should raise error for invalid fraction/decimal
    with pytest.raises(ValueError) as excinfo:
        model.add_recipe(
            title="Bread",
            instructions="Bake",
            measurement="abc"
        )
    assert "Invalid measurement" in str(excinfo.value)

def test_update_recipe_invalid_measurement(model):
    # Create a valid recipe
    recipe_id = model.add_recipe(
        title="Pie",
        instructions="Bake",
        measurement="2"
    )
    # Update with invalid measurement
    with pytest.raises(ValueError) as excinfo:
        model.update_recipe(recipe_id, measurement="not_a_fraction")
    assert "Invalid measurement" in str(excinfo.value)

def test_add_sticker_blank_name(model):
    # Should require both name and imageURL
    with pytest.raises(ValueError) as excinfo:
        model.add_sticker(name="", imageURL="http://img.com/1.png")
    assert "Both name and imageURL" in str(excinfo.value)

def test_add_sticker_missing_url(model):
    with pytest.raises(ValueError) as excinfo:
        model.add_sticker(name="Fun", imageURL=None)
    assert "Both name and imageURL" in str(excinfo.value)

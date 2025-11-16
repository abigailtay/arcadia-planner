"""
File: tests/RecipeBox/test_recipebox_api.py
Author: Allyson Taylor
Date: 2025-11-13
Description:
    Full integration tests for Recipe Box backend:
    CRUD, category/subcategory filter, stickers, fractional measurement,
    with API response logging.
"""

import sys
import os
import pytest
import sqlite3
import logging

# Add project root folder to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from controllers.recipebox import app

# Configure logging to file for API response logging
logging.basicConfig(
    filename='tests/RecipeBox/recipebox_api_test_log.txt',
    level=logging.INFO,
    format='%(message)s'
)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def log_response(resp):
    logging.info(f"Status: {resp.status_code}")
    logging.info(f"Response JSON: {resp.get_json()}")

def create_sticker(client):
    """
    Helper function to create a sticker and return its stickerId.
    """
    resp = client.post('/stickers', json={
        "name": "Vegan",
        "imageURL": "https://example.com/vegan.png"
    })
    log_response(resp)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "stickerId" in data
    return data["stickerId"]

def test_create_sticker(client):
    """
    Test sticker creation, verifying both name and imageURL must be provided.
    """
    create_sticker(client)

def test_recipe_crud_and_filter(client):
    """
    Full scenario test for Recipe Box CRUD and filtering with stickers and fractional measurement.
    """

    # Setup: create category and subcategory via direct SQL with conflict handling
    with sqlite3.connect('arcadia.db') as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', ('Main',))
        conn.commit()
        c.execute('SELECT categoryId FROM categories WHERE name=?', ('Main',))
        category_id = c.fetchone()[0]

        c.execute('INSERT OR IGNORE INTO subcategories (categoryId, name) VALUES (?, ?)', (category_id, 'Desserts'))
        conn.commit()
        c.execute('SELECT subcategoryId FROM subcategories WHERE categoryId=? AND name=?', (category_id, 'Desserts'))
        subcat_id = c.fetchone()[0]

    # Create sticker using API and get its ID
    sticker_id = create_sticker(client)

    # Create a new recipe linked to created category, subcategory, and sticker
    recipe_payload = {
        'title': 'Apple Pie',
        'instructions': 'Mix and bake.',
        'categoryId': category_id,
        'subcategoryId': subcat_id,
        'stickerId': sticker_id,
        'measurement': '3/4'
    }
    resp_create = client.post('/recipes', json=recipe_payload)
    log_response(resp_create)
    assert resp_create.status_code == 201
    recipe_id = resp_create.json['recipeId']

    # Retrieve the newly created recipe by ID
    resp_view = client.get(f'/recipes/{recipe_id}')
    log_response(resp_view)
    assert resp_view.status_code == 200
    assert resp_view.json['recipe']['title'] == 'Apple Pie'

    # Filter recipes by category and subcategory
    resp_filter = client.get(f'/recipes?categoryId={category_id}&subcategoryId={subcat_id}')
    log_response(resp_filter)
    assert resp_filter.status_code == 200
    assert any(r['recipeId'] == recipe_id for r in resp_filter.json['recipes'])

    # Update recipe title and fractional measurement
    resp_update = client.put(f'/recipes/{recipe_id}', json={'title': 'Cherry Pie', 'measurement': '2/3'})
    log_response(resp_update)
    assert resp_update.status_code == 200

    # Delete the recipe
    resp_delete = client.delete(f'/recipes/{recipe_id}')
    log_response(resp_delete)
    assert resp_delete.status_code == 200

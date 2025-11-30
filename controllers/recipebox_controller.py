"""
File: recipebox_controller.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    REST API endpoints for Recipe Box module.
    All logic routed to RecipeBoxModel for CRUD, filtering, fraction formatting, sticker management.
"""

from flask import Flask, request, jsonify
from models.recipeboxmodel import RecipeBoxModel

app = Flask(__name__)
recipe_model = RecipeBoxModel()

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    try:
        recipe_id = recipe_model.add_recipe(
            title=data.get('title'),
            instructions=data.get('instructions'),
            categoryId=data.get('categoryId'),
            subcategoryId=data.get('subcategoryId'),
            stickerId=data.get('stickerId'),
            measurement=data.get('measurement')
        )
    except ValueError as e:
        return jsonify(success=False, error=str(e)), 400
    return jsonify(success=True, recipeId=recipe_id), 201

@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.get_json()
    try:
        recipe_model.update_recipe(recipe_id, **data)
    except ValueError as e:
        return jsonify(success=False, error=str(e)), 400
    return jsonify(success=True), 200

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    recipe = recipe_model.get_recipe(recipe_id)
    if not recipe:
        return jsonify(success=False, error='Recipe not found'), 404
    return jsonify(success=True, recipe=recipe), 200

@app.route('/recipes', methods=['GET'])
def filter_recipes():
    categoryId = request.args.get('categoryId')
    subcategoryId = request.args.get('subcategoryId')
    recipes = recipe_model.filter_recipes(categoryId, subcategoryId)
    return jsonify(success=True, recipes=recipes), 200

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe_model.delete_recipe(recipe_id)
    return jsonify(success=True), 200

@app.route('/stickers', methods=['POST'])
def add_sticker():
    data = request.get_json()
    try:
        sticker_id = recipe_model.add_sticker(data.get('name'), data.get('imageURL'))
    except ValueError as e:
        return jsonify(success=False, error=str(e)), 400
    return jsonify(success=True, stickerId=sticker_id), 201

if __name__ == '__main__':
    app.run(debug=True, port=5002)

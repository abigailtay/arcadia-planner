"""
File: controllers/recipebox.py
Author: Allyson Taylor
Date: 2025-11-13
Description:
    REST API endpoints for Recipe Box with CRUD functionality,
    filtering by category/subcategory, sticker assignment,
    support for fractional ingredient measurement (internal decimal, external fraction format),
    and sticker creation requiring user-provided image URL.
"""

from flask import Flask, request, jsonify
import sqlite3
from fractions import Fraction

app = Flask(__name__)
DB_PATH = 'arcadia.db'

def get_conn():
    return sqlite3.connect(DB_PATH, timeout=10)

def format_fraction(value):
    try:
        f = Fraction(str(value)).limit_denominator(16)
        return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
    except Exception:
        return str(value)

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    if not data.get('title'):
        return jsonify(success=False, error='Title required'), 400
    measurement = None
    if 'measurement' in data:
        try:
            measurement = float(Fraction(data['measurement']))
        except Exception:
            return jsonify(success=False, error='Invalid measurement format'), 400
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO recipes (title, instructions, categoryId, subcategoryId, stickerId, measurement)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (data['title'], data.get('instructions'), data.get('categoryId'),
                   data.get('subcategoryId'), data.get('stickerId'), measurement))
        r_id = c.lastrowid
        conn.commit()
    return jsonify(success=True, recipeId=r_id), 201

@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.get_json()
    fields = []
    vals = []
    for k in ['title', 'instructions', 'categoryId', 'subcategoryId', 'stickerId']:
        if k in data:
            fields.append(f"{k}=?")
            vals.append(data[k])
    if 'measurement' in data:
        try:
            measurement_val = float(Fraction(data['measurement']))
        except Exception:
            return jsonify(success=False, error='Invalid measurement format'), 400
        fields.append("measurement=?")
        vals.append(measurement_val)
    if not fields:
        return jsonify(success=False, error='No valid fields to update'), 400
    vals.append(recipe_id)
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(f"UPDATE recipes SET {', '.join(fields)} WHERE recipeId=?", vals)
        conn.commit()
    return jsonify(success=True), 200

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''SELECT recipeId, title, instructions, categoryId, subcategoryId, stickerId, measurement FROM recipes WHERE recipeId=?''', (recipe_id,))
        row = c.fetchone()
    if not row:
        return jsonify(success=False, error='Recipe not found'), 404
    recipe = {
        'recipeId': row[0],
        'title': row[1],
        'instructions': row[2],
        'categoryId': row[3],
        'subcategoryId': row[4],
        'stickerId': row[5],
        'measurement': format_fraction(row[6]) if row[6] is not None else None
    }
    return jsonify(success=True, recipe=recipe), 200

@app.route('/recipes', methods=['GET'])
def filter_recipes():
    categoryId = request.args.get('categoryId')
    subcategoryId = request.args.get('subcategoryId')
    where_clause = []
    vals = []
    if categoryId:
        where_clause.append('categoryId=?')
        vals.append(categoryId)
    if subcategoryId:
        where_clause.append('subcategoryId=?')
        vals.append(subcategoryId)
    query = 'SELECT recipeId, title, categoryId, subcategoryId, stickerId, measurement FROM recipes'
    if where_clause:
        query += ' WHERE ' + ' AND '.join(where_clause)
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(query, vals)
        rows = c.fetchall()
        recipes = [{
            'recipeId': r[0], 'title': r[1], 'categoryId': r[2], 'subcategoryId': r[3],
            'stickerId': r[4], 'measurement': format_fraction(r[5]) if r[5] else None
        } for r in rows]
    return jsonify(success=True, recipes=recipes), 200

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM recipes WHERE recipeId=?', (recipe_id,))
        conn.commit()
    return jsonify(success=True), 200

@app.route('/stickers', methods=['POST'])
def add_sticker():
    """
    Endpoint to add a new sticker. User must supply 'name' and 'imageURL'.
    """
    data = request.get_json()
    name = data.get('name')
    imageURL = data.get('imageURL')
    if not name or not imageURL:
        return jsonify(success=False, error='Both name and imageURL are required'), 400
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO stickers (name, imageURL) VALUES (?, ?)', (name, imageURL))
        sticker_id = c.lastrowid
        conn.commit()
    return jsonify(success=True, stickerId=sticker_id), 201

if __name__ == '__main__':
    app.run(debug=True, port=5002)

"""
File: recipeboxmodel.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Backend logic for Recipe Box: CRUD, category/subcategory filtering, sticker creation, measurements as decimals/fractions.
"""

import sqlite3
from fractions import Fraction

DB_PATH = 'arcadia.db'

def format_fraction(value):
    try:
        f = Fraction(str(value)).limit_denominator(16)
        return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
    except Exception:
        return str(value)

class RecipeBoxModel:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=10)

    def add_recipe(self, title, instructions=None, categoryId=None, subcategoryId=None, stickerId=None, measurement=None):
        measurement_val = None
        if measurement is not None:
            try:
                measurement_val = float(Fraction(str(measurement)))
            except Exception:
                raise ValueError('Invalid measurement format')
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(
                '''INSERT INTO recipes (title, instructions, categoryId, subcategoryId, stickerId, measurement)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (title, instructions, categoryId, subcategoryId, stickerId, measurement_val)
            )
            recipe_id = c.lastrowid
            conn.commit()
        return recipe_id

    def update_recipe(self, recipe_id, **fields):
        allowed_keys = ['title', 'instructions', 'categoryId', 'subcategoryId', 'stickerId', 'measurement']
        updates = []
        vals = []
        for k in allowed_keys:
            if k in fields:
                if k == 'measurement':
                    try:
                        vals.append(float(Fraction(str(fields[k]))))
                    except Exception:
                        raise ValueError('Invalid measurement format')
                    updates.append("measurement=?")
                else:
                    updates.append(f"{k}=?")
                    vals.append(fields[k])
        if not updates:
            raise ValueError('No valid fields to update')
        vals.append(recipe_id)
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(f"UPDATE recipes SET {', '.join(updates)} WHERE recipeId=?", vals)
            conn.commit()

    def get_recipe(self, recipe_id):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('''SELECT recipeId, title, instructions, categoryId, subcategoryId, stickerId, measurement FROM recipes WHERE recipeId=?''', (recipe_id,))
            row = c.fetchone()
        if not row:
            return None
        return {
            'recipeId': row[0],
            'title': row[1],
            'instructions': row[2],
            'categoryId': row[3],
            'subcategoryId': row[4],
            'stickerId': row[5],
            'measurement': format_fraction(row[6]) if row[6] is not None else None
        }

    def filter_recipes(self, categoryId=None, subcategoryId=None):
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
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(query, vals)
            rows = c.fetchall()
        recipes = [{
            'recipeId': r[0], 'title': r[1], 'categoryId': r[2], 'subcategoryId': r[3],
            'stickerId': r[4], 'measurement': format_fraction(r[5]) if r[5] else None
        } for r in rows]
        return recipes

    def delete_recipe(self, recipe_id):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM recipes WHERE recipeId=?', (recipe_id,))
            conn.commit()

    def add_sticker(self, name, imageURL):
        if not name or not imageURL:
            raise ValueError('Both name and imageURL required')
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('INSERT INTO stickers (name, imageURL) VALUES (?, ?)', (name, imageURL))
            sticker_id = c.lastrowid
            conn.commit()
        return sticker_id

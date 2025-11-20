"""
File: avatarstoremodel.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Backend logic for avatar store purchases,
    currency deduction, unlock mechanics, and inventory management.
"""

import sqlite3

DB_PATH = "arcadia.db"

class AvatarStoreModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_user_glitter(self, user_id:int) -> int:
        self.cursor.execute("SELECT glitter FROM user WHERE userId=?", (user_id,))
        row = self.cursor.fetchone()
        return row['glitter'] if row else 0

    def get_item_cost(self, item_id:int) -> int:
        self.cursor.execute("SELECT glitterCost FROM store_items WHERE itemId=?", (item_id,))
        row = self.cursor.fetchone()
        return row['glitterCost'] if row else None

    def purchase_item(self, user_id:int, item_id:int) -> bool:
        cost = self.get_item_cost(item_id)
        if cost is None:
            return False  # Item doesn't exist

        user_glitter = self.get_user_glitter(user_id)
        if user_glitter < cost:
            return False  # Not enough glitter

        # Deduct glitter and add item to inventory
        try:
            self.cursor.execute("UPDATE user SET glitter = glitter - ? WHERE userId=?", (cost, user_id))
            self.cursor.execute(
                "INSERT INTO user_inventory (userId, itemId) VALUES (?, ?)",
                (user_id, item_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error in purchase_item: {e}")
            return False

    def get_user_inventory(self, user_id:int):
        self.cursor.execute(
            """SELECT si.* FROM store_items si
               JOIN user_inventory ui ON si.itemId = ui.itemId
               WHERE ui.userId = ?""", (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

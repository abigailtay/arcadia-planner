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
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_user_glitter(self, user_id:int) -> int:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT glitter FROM user WHERE userId=?", (user_id,))
            row = cur.fetchone()
            return row['glitter'] if row else 0

    def get_item_cost(self, item_id:int) -> int:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT glitterCost FROM store_items WHERE itemId=?", (item_id,))
            row = cur.fetchone()
            return row['glitterCost'] if row else None

    def purchase_item(self, user_id:int, item_id:int) -> bool:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cost = self.get_item_cost(item_id)
            if cost is None:
                return False
            # Check unavailable
            cur.execute("SELECT available FROM store_items WHERE itemId=?", (item_id,))
            row = cur.fetchone()
            if not row or row['available'] == 0:
                return False
            # Check duplicate (already owned)
            cur.execute("SELECT 1 FROM user_inventory WHERE userId=? AND itemId=?", (user_id, item_id))
            if cur.fetchone():
                return False
            user_glitter = self.get_user_glitter(user_id)
            if user_glitter < cost:
                return False  # Not enough glitter
            try:
                cur.execute("UPDATE user SET glitter = glitter - ? WHERE userId=?", (cost, user_id))
                cur.execute(
                    "INSERT INTO user_inventory (userId, itemId) VALUES (?, ?)",
                    (user_id, item_id)
                )
                conn.commit()
                return True
            except Exception as e:
                print(f"Error in purchase_item: {e}")
                return False

    def get_user_inventory(self, user_id:int):
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT si.* FROM store_items si
                   JOIN user_inventory ui ON si.itemId = ui.itemId
                   WHERE ui.userId = ?""", (user_id,))
            return cur.fetchall()

    def close(self):
        pass  

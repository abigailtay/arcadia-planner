"""
File: budgetmodel.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Core backend logic for Budget module.
    Handles CRUD operations for transactions and analytics calculations (sum, average, by category) using arcadia.db.
"""

import sqlite3

DB_PATH = 'arcadia.db'

class BudgetModel:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        return conn

    def add_transaction(self, name, amount, category, trans_type):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO transactions (name, amount, category, type) VALUES (?, ?, ?, ?)',
                (name, amount, category, trans_type)
            )
            transaction_id = c.lastrowid
            conn.commit()
        return transaction_id

    def update_transaction(self, transaction_id, **fields):
        updates = []
        values = []
        for field in ['name', 'amount', 'category', 'type']:
            if field in fields:
                updates.append(f"{field}=?")
                values.append(fields[field])
        if not updates:
            return False
        values.append(transaction_id)
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(
                f'UPDATE transactions SET {", ".join(updates)} WHERE transactionId=?', values
            )
            conn.commit()
        return True

    def get_transaction(self, transaction_id):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(
                'SELECT transactionId, name, amount, category, type, timestamp FROM transactions WHERE transactionId=?',
                (transaction_id,)
            )
            row = c.fetchone()
        if not row:
            return None
        keys = ['transactionId', 'name', 'amount', 'category', 'type', 'timestamp']
        return dict(zip(keys, row))

    def list_transactions(self):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(
                'SELECT transactionId, name, amount, category, type, timestamp FROM transactions'
            )
            rows = c.fetchall()
        keys = ['transactionId', 'name', 'amount', 'category', 'type', 'timestamp']
        return [dict(zip(keys, row)) for row in rows]

    def delete_transaction(self, transaction_id):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM transactions WHERE transactionId=?', (transaction_id,))
            conn.commit()
        return True

    def analytics(self, trans_type=None, category=None):
        query = 'SELECT amount, category, type FROM transactions'
        filters = []
        params = []
        if trans_type:
            filters.append("type=?")
            params.append(trans_type)
        if category:
            filters.append("category=?")
            params.append(category)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(query, params)
            rows = c.fetchall()
        amounts = [r[0] for r in rows]
        if not amounts:
            return None
        summary = {
            'sum': sum(amounts),
            'average': sum(amounts) / len(amounts),
            'by_category': {}
        }
        for amt, cat, typ in rows:
            if cat not in summary['by_category']:
                summary['by_category'][cat] = {'sum': 0, 'count': 0}
            summary['by_category'][cat]['sum'] += amt
            summary['by_category'][cat]['count'] += 1
        return summary

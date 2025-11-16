"""
File: controllers/budget.py
Author: Allyson Taylor
Date: 2025-11-16
Description:
    REST API endpoints for Budget module handling CRUD operations for transactions (create, read, update, delete)
    and analytics logic (total sum, average, category breakdown). Uses arcadia.db as database.
"""

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = 'arcadia.db'

def get_conn():
    return sqlite3.connect(DB_PATH, timeout=10)

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    name = data.get('name')
    amount = data.get('amount')
    category = data.get('category')
    trans_type = data.get('type')
    if not name or amount is None or not category or trans_type not in ('expense', 'income'):
        return jsonify(success=False, error='Missing or invalid fields'), 400
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO transactions (name, amount, category, type) VALUES (?, ?, ?, ?)',
                  (name, amount, category, trans_type))
        transaction_id = c.lastrowid
        conn.commit()
    return jsonify(success=True, transactionId=transaction_id), 201

@app.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    updates = []
    values = []
    for field in ['name', 'amount', 'category', 'type']:
        if field in data:
            updates.append(f"{field}=?")
            values.append(data[field])
    if not updates:
        return jsonify(success=False, error='No fields to update'), 400
    values.append(transaction_id)
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(f"UPDATE transactions SET {', '.join(updates)} WHERE transactionId=?", values)
        conn.commit()
    return jsonify(success=True), 200

@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def view_transaction(transaction_id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT transactionId, name, amount, category, type, timestamp FROM transactions WHERE transactionId=?', (transaction_id,))
        row = c.fetchone()
    if not row:
        return jsonify(success=False, error='Transaction not found'), 404
    resp = dict(zip(['transactionId', 'name', 'amount', 'category', 'type', 'timestamp'], row))
    return jsonify(success=True, transaction=resp), 200

@app.route('/transactions', methods=['GET'])
def list_transactions():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT transactionId, name, amount, category, type, timestamp FROM transactions')
        rows = c.fetchall()
        transactions = [dict(zip(['transactionId', 'name', 'amount', 'category', 'type', 'timestamp'], r)) for r in rows]
    return jsonify(success=True, transactions=transactions), 200

@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM transactions WHERE transactionId=?', (transaction_id,))
        conn.commit()
    return jsonify(success=True), 200

@app.route('/analytics', methods=['GET'])
def analytics():
    # Accept ?type=(expense/income) and/or ?category=...
    query = 'SELECT amount, category, type FROM transactions'
    filters = []
    params = []
    if 'type' in request.args:
        filters.append("type=?")
        params.append(request.args['type'])
    if 'category' in request.args:
        filters.append("category=?")
        params.append(request.args['category'])
    if filters:
        query += " WHERE " + " AND ".join(filters)
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(query, params)
        rows = c.fetchall()
    amounts = [r[0] for r in rows]
    if not amounts:
        return jsonify(success=True, summary=None), 200
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
    return jsonify(success=True, summary=summary), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)

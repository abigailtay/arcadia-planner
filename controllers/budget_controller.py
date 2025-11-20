"""
File: budget_controller.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    REST API endpoints for Budget module, calling BudgetModel for CRUD operations and analytics.
    Input/output validation and error handling.
"""

from flask import Flask, request, jsonify
from models.budgetmodel import BudgetModel

app = Flask(__name__)
budget_model = BudgetModel()

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    name = data.get('name')
    amount = data.get('amount')
    category = data.get('category')
    trans_type = data.get('type')
    if not name or amount is None or not category or trans_type not in ('expense', 'income'):
        return jsonify(success=False, error='Missing or invalid fields'), 400
    transaction_id = budget_model.add_transaction(name, amount, category, trans_type)
    return jsonify(success=True, transactionId=transaction_id), 201

@app.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    fields = {k: data[k] for k in ['name', 'amount', 'category', 'type'] if k in data}
    if not fields:
        return jsonify(success=False, error='No fields to update'), 400
    ok = budget_model.update_transaction(transaction_id, **fields)
    if not ok:
        return jsonify(success=False, error='No valid fields'), 400
    return jsonify(success=True), 200

@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def view_transaction(transaction_id):
    result = budget_model.get_transaction(transaction_id)
    if not result:
        return jsonify(success=False, error='Transaction not found'), 404
    return jsonify(success=True, transaction=result), 200

@app.route('/transactions', methods=['GET'])
def list_transactions():
    transactions = budget_model.list_transactions()
    return jsonify(success=True, transactions=transactions), 200

@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    budget_model.delete_transaction(transaction_id)
    return jsonify(success=True), 200

@app.route('/analytics', methods=['GET'])
def analytics():
    trans_type = request.args.get('type')
    category = request.args.get('category')
    summary = budget_model.analytics(trans_type, category)
    return jsonify(success=True, summary=summary), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)

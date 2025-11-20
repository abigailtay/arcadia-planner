"""
File: avatarstore_controller.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    REST API endpoints for Avatar Store purchases, currency deduction,
    inventory lookups, and unlock logic.
    Relies on AvatarStoreModel for all business logic.
"""

from flask import Flask, request, jsonify
from models.avatarstoremodel import AvatarStoreModel

app = Flask(__name__)
store_model = AvatarStoreModel()

@app.route('/store/purchase', methods=['POST'])
def purchase_item():
    data = request.get_json()
    user_id = data.get('userId')
    item_id = data.get('itemId')
    if not user_id or not item_id:
        return jsonify({'success': False, 'error': 'userId and itemId required'}), 400
    result = store_model.purchase_item(user_id, item_id)
    if result:
        return jsonify({'success': True, 'message': 'Purchase successful.'}), 200
    else:
        return jsonify({'success': False, 'error': 'Not enough glitter or item not found.'}), 400

@app.route('/store/inventory/<int:user_id>', methods=['GET'])
def user_inventory(user_id):
    inventory = store_model.get_user_inventory(user_id)
    # Ensure fetched rows are dicts
    output = [dict(item) for item in inventory]
    return jsonify({'success': True, 'inventory': output}), 200

@app.route('/store/glitter/<int:user_id>', methods=['GET'])
def user_glitter(user_id):
    glitter = store_model.get_user_glitter(user_id)
    return jsonify({'success': True, 'userId': user_id, 'glitter': glitter}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5004)

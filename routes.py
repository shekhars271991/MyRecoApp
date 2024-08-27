from flask import Blueprint, request, jsonify
from service.db.products import get_all_products, add_product, get_product_by_sku
from service.db.redis import load_sample_products
from flask_jwt_extended import jwt_required


api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/add_product', methods=['POST'])
@jwt_required()
def add_product_route():
    data = request.get_json()

    # Validation for required fields
    required_fields = ['name', 'sku', 'price', 'categories']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate that categories is a list
    if not isinstance(data['categories'], list):
        return jsonify({'error': 'categories must be a list'}), 400

    # Check if a product with the same SKU already exists
    existing_product = get_product_by_sku(data['sku'])
    if existing_product:
        return jsonify({'error': f'Product with SKU {data["sku"]} already exists'}), 400

    new_product = {
        'name': data['name'],
        'sku': data['sku'],
        'description': data.get('description', ''),
        'categories': data['categories'],
        'price': data['price']
    }
    add_product(new_product)
    return jsonify({'message': 'Product added successfully'}), 201

@api_bp.route('/get_products', methods=['GET'])
@jwt_required()
def get_products_route():
    products = get_all_products()
    return jsonify(products), 200

@api_bp.route('/load_sample_products', methods=['POST'])
def load_sample_products_route():
    load_sample_products()
    return jsonify({'message': 'Sample products loaded successfully'}), 200

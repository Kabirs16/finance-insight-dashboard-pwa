"""
Finance App - Flask API Backend
Connects HTML frontend with Python SQLite database
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
from finance_app_backend import FinanceApp

app = Flask(__name__, static_folder='web_frontend', static_url_path='')
CORS(app)

# Initialize the finance app
finance_app = FinanceApp("finance_app.db")

# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get complete dashboard data"""
    days = request.args.get('days', 30, type=int)
    summary = finance_app.analytics.get_financial_summary(days)
    
    return jsonify({
        'summary': summary,
        'expense_breakdown': finance_app.analytics.get_expense_breakdown(days),
        'income_breakdown': finance_app.analytics.get_income_breakdown(days),
        'monthly_trend': finance_app.analytics.get_monthly_trend(6),
        'top_expenses': finance_app.analytics.get_top_expenses(5, days),
        'top_income': finance_app.analytics.get_top_income_sources(5, days),
        'product_analytics': finance_app.analytics.get_product_analytics()
    })

@app.route('/api/visualization-data', methods=['GET'])
def get_visualization_data():
    """Get data formatted for charts"""
    return jsonify(finance_app.exporter.get_visualization_data())

# ============================================================================
# PRODUCTS ENDPOINTS
# ============================================================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    category = request.args.get('category')
    products = finance_app.products.get_all_products(category)
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create new product"""
    data = request.json
    result = finance_app.products.add_product(
        name=data.get('name'),
        price=data.get('price'),
        quantity=data.get('quantity', 0),
        category=data.get('category', 'General'),
        description=data.get('description', '')
    )
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product"""
    product = finance_app.products.get_product(product_id)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product"""
    data = request.json
    result = finance_app.products.update_product(product_id, **data)
    return jsonify(result)

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product"""
    result = finance_app.products.delete_product(product_id)
    return jsonify(result)

# ============================================================================
# EXPENSES ENDPOINTS
# ============================================================================

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """Get expenses"""
    days = request.args.get('days', 30, type=int)
    expenses = finance_app.expenses.get_expenses(days)
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def create_expense():
    """Create expense"""
    data = request.json
    result = finance_app.expenses.add_expense(
        category=data.get('category'),
        amount=data.get('amount'),
        description=data.get('description', ''),
        payment_method=data.get('payment_method', 'cash')
    )
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete expense"""
    result = finance_app.expenses.delete_expense(expense_id)
    return jsonify(result)

# ============================================================================
# INCOME ENDPOINTS
# ============================================================================

@app.route('/api/income', methods=['GET'])
def get_income():
    """Get income"""
    days = request.args.get('days', 30, type=int)
    income = finance_app.income.get_income(days)
    return jsonify(income)

@app.route('/api/income', methods=['POST'])
def create_income():
    """Create income"""
    data = request.json
    result = finance_app.income.add_income(
        source=data.get('source'),
        amount=data.get('amount'),
        description=data.get('description', ''),
        income_type=data.get('income_type', 'regular')
    )
    return jsonify(result), 201 if result['success'] else 400

# ============================================================================
# CART ENDPOINTS
# ============================================================================

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get cart items"""
    return jsonify(finance_app.cart.get_cart())

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.json
    result = finance_app.cart.add_to_cart(
        product_id=data.get('product_id'),
        quantity=data.get('quantity', 1)
    )
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/cart/<int:cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    """Remove item from cart"""
    result = finance_app.cart.remove_from_cart(cart_id)
    return jsonify(result)

@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    """Checkout cart"""
    result = finance_app.cart.checkout()
    return jsonify(result)

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Finance App API is running',
        'timestamp': datetime.now().isoformat()
    })

# ============================================================================
# ROOT ROUTE (Serve web frontend)
# ============================================================================

@app.route('/')
def index():
    """Serve index.html"""
    return send_from_directory('web_frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('web_frontend', path)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True, port=8080, host='0.0.0.0')
    finally:
        finance_app.close()

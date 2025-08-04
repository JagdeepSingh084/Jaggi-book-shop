from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# In-memory cart storage (in production, use a database)
cart = {}

def load_cart():
    """Load cart data from a JSON file if it exists."""
    try:
        with open('cart.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cart(cart_data):
    """Save cart data to a JSON file."""
    with open('cart.json', 'w') as f:
        json.dump(cart_data, f)

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get current cart contents."""
    return jsonify(cart)

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart."""
    try:
        data = request.get_json()
        upc = data.get('upc')
        quantity = data.get('quantity', 1)
        
        if not upc:
            return jsonify({'error': 'UPC is required'}), 400
            
        if upc in cart:
            cart[upc]['quantity'] += quantity
        else:
            cart[upc] = {
                'quantity': quantity
            }
            
        save_cart(cart)
        return jsonify(cart)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Serve index.html."""
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_file(path):
    """Serve static files."""
    return app.send_static_file(path)

if __name__ == '__main__':
    # Load existing cart data if it exists
    cart = load_cart()
    app.run(debug=True)

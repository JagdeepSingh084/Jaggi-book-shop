from flask import Flask, jsonify, send_from_directory, render_template, request, session, redirect, url_for
import json
import os

app = Flask(__name__, static_folder='output', template_folder='templates')
app.secret_key = 'jaggi_books_secret_key'  # Required for session management

# Load data
def load_data():
    with open('data/categories.json', 'r') as f:
        categories = json.load(f)
    with open('data/all_books.json', 'r') as f:
        books = json.load(f)
    return categories, books

# API Routes
@app.route('/api/categories')
def get_categories():
    categories, _ = load_data()
    return jsonify(categories)

@app.route('/api/books')
def get_books():
    _, books = load_data()
    return jsonify(books)

@app.route('/api/category/<category_slug>')
def get_category_books(category_slug):
    _, books = load_data()
    category_books = [book for book in books if book['category_slug'] == category_slug]
    return jsonify(category_books)

@app.route('/api/book/<upc>')
def get_book(upc):
    _, books = load_data()
    book = next((book for book in books if book['upc'] == upc), None)
    if book:
        return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

# Cart API endpoints
@app.route('/api/cart', methods=['GET'])
def get_cart():
    cart = session.get('cart', [])
    return jsonify(cart)

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    upc = data.get('upc')
    quantity = int(data.get('quantity', 1))
    
    # Ensure book data exists
    book = next((b for b in all_books if b['upc'] == upc), None)
    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), 404
    
    # Initialize cart if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    # Append or update quantity if item exists
    if upc in session['cart']:
        session['cart'][upc]['quantity'] += quantity
    else:
        session['cart'][upc] = {
            'title': book['title'],
            'price': float(book['price']),
            'quantity': quantity,
            'image': book['image']
        }
    
    session.modified = True
    return jsonify({'success': True, 'cart': session['cart']})

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    upc = data.get('upc')
    
    if not upc:
        return jsonify({'error': 'UPC is required'}), 400
    
    cart = session.get('cart', [])
    cart = [item for item in cart if item['upc'] != upc]
    session['cart'] = cart
    
    return jsonify(cart)

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    upc = data.get('upc')
    quantity = data.get('quantity')
    
    if not upc or quantity is None:
        return jsonify({'error': 'UPC and quantity are required'}), 400
    
    cart = session.get('cart', [])
    item_exists = False
    
    # Check for existing item in cart
    for item in cart:
        if item['upc'] == upc:
            item['quantity'] += 1
            item_exists = True
            break
    
    if not item_exists:
        cart.append({
            'upc': upc,
            'title': book['title'],
            'price': book['price'],
            'quantity': 1,
            'image_url': book['image_url']
        })
    
    session['cart'] = cart
    return jsonify({
        'success': True,
        'message': 'Item added to cart',
        'cart_item': cart[-1],
        'cart_count': len(cart)
    })

# Web Routes
@app.route('/')
def index():
    return send_from_directory('output', 'index.html')

@app.route('/book/<upc>')
def book_detail(upc):
    return send_from_directory('output', f'book_{upc}.html')

@app.route('/category/<category_slug>')
def category_detail(category_slug):
    return send_from_directory('output', f'category_{category_slug}.html')

@app.route('/cart')
def cart():
    return send_from_directory('output', 'cart.html')

# New page routes
@app.route('/new-arrivals')
def new_arrivals():
    return send_from_directory('output', 'new_arrivals.html')

@app.route('/bestsellers')
def bestsellers():
    return send_from_directory('output', 'bestsellers.html')

@app.route('/special-offers')
def special_offers():
    return send_from_directory('output', 'special_offers.html')

@app.route('/about')
def about():
    return send_from_directory('output', 'about.html')

@app.route('/contact')
def contact():
    return send_from_directory('output', 'contact.html')

@app.route('/faq')
def faq():
    return send_from_directory('output', 'faq.html')

@app.route('/checkout')
def checkout():
    return send_from_directory('output', 'checkout.html')

# Add a new API endpoint to clear the cart
@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    session['cart'] = []
    return jsonify([])

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('output', path)

if __name__ == '__main__':
    app.run(debug=True)
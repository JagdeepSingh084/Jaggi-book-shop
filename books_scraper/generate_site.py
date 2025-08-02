import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader

# Load data
def load_data():
    with open('data/categories.json', 'r') as f:
        categories = json.load(f)
    
    with open('data/all_books.json', 'r') as f:
        books = json.load(f)
    
    return categories, books

# Create output directory
def create_output_dir():
    os.makedirs('output', exist_ok=True)
    os.makedirs('output/images', exist_ok=True)
    os.makedirs('output/static/css', exist_ok=True)
    os.makedirs('output/static/js', exist_ok=True)

# Copy static files
def copy_static_files():
    # Copy CSS
    shutil.copy('static/css/styles.css', 'output/static/css/')
    
    # Copy JavaScript
    if os.path.exists('static/js/cart.js'):
        shutil.copy('static/js/cart.js', 'output/static/js/')
    
    # Copy images
    for filename in os.listdir('images'):
        shutil.copy(f'images/{filename}', f'output/images/')

# Generate HTML files
def generate_html_files(categories, books):
    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader('templates'))
    
    # Generate index page
    template = env.get_template('index.html')
    with open('output/index.html', 'w', encoding='utf-8') as f:
        f.write(template.render(categories=categories, books=books))
    
    # Generate category pages
    template = env.get_template('category.html')
    for category in categories:
        category_books = [book for book in books if book['category_slug'] == category['slug']]
        with open(f'output/category_{category["slug"]}.html', 'w', encoding='utf-8') as f:
            f.write(template.render(
                categories=categories,
                category=category,
                category_books=category_books
            ))
    
    # Generate book detail pages
    template = env.get_template('book.html')
    for book in books:
        with open(f'output/book_{book["upc"]}.html', 'w', encoding='utf-8') as f:
            f.write(template.render(categories=categories, book=book))
    
    # Generate cart page
    template = env.get_template('cart.html')
    with open('output/cart.html', 'w', encoding='utf-8') as f:
        f.write(template.render(categories=categories))
    
    # Generate pagination pages
    template = env.get_template('index.html')
    books_per_page = 20
    total_pages = (len(books) + books_per_page - 1) // books_per_page
    
    for page in range(2, total_pages + 1):
        start_idx = (page - 1) * books_per_page
        end_idx = start_idx + books_per_page
        page_books = books[start_idx:end_idx]
        
        with open(f'output/page_{page}.html', 'w', encoding='utf-8') as f:
            f.write(template.render(
                categories=categories,
                books=page_books,
                current_page=page,
                total_pages=total_pages
            ))

# Main function
def generate_site():
    print("Starting to generate static site...")
    
    # Load data
    categories, books = load_data()
    
    # Create output directory
    create_output_dir()
    
    # Copy static files
    copy_static_files()
    
    # Generate HTML files
    generate_html_files(categories, books)
    
    print("Static site generation completed successfully!")
    print(f"Site available at: {os.path.abspath('output/index.html')}")

if __name__ == "__main__":
    generate_site()
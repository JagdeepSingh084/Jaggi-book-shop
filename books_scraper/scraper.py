import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

# Base URLs
BASE_URL = 'https://books.toscrape.com/'
CATALOGUE_URL = urljoin(BASE_URL, 'catalogue/')

# Create directories for data and images
os.makedirs('books_scraper/data', exist_ok=True)
os.makedirs('books_scraper/images', exist_ok=True)

# Function to sanitize filenames
def sanitize_filename(name):
    return ''.join(c if c.isalnum() or c in ['-', '_'] else '_' for c in name)

# Function to download and save an image
def save_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'books_scraper/images/{filename}', 'wb') as f:
            f.write(response.content)
        return filename
    return None

# Function to extract categories
def extract_categories():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    categories = []
    category_nav = soup.select_one('.side_categories > ul > li > ul')
    
    if category_nav:
        for category_li in category_nav.select('li'):
            category_a = category_li.select_one('a')
            if category_a:
                category_name = category_a.text.strip()
                category_url = urljoin(BASE_URL, category_a['href'])
                categories.append({
                    'name': category_name,
                    'url': category_url,
                    'slug': sanitize_filename(category_name.lower())
                })
    
    return categories

# Function to extract book details from a product page
def extract_book_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract main details
    title = soup.select_one('h1').text.strip() if soup.select_one('h1') else 'Unknown Title'
    
    # Extract product information
    product_info = {}
    product_table = soup.select_one('table.table-striped')
    if product_table:
        for row in product_table.select('tr'):
            header = row.select_one('th').text.strip() if row.select_one('th') else ''
            value = row.select_one('td').text.strip() if row.select_one('td') else ''
            product_info[header] = value
    
    # Extract price
    price_div = soup.select_one('p.price_color')
    price = price_div.text.strip() if price_div else 'Unknown Price'
    
    # Extract availability
    availability_div = soup.select_one('p.availability')
    availability = availability_div.text.strip() if availability_div else 'Unknown Availability'
    
    # Extract description
    description_div = soup.select_one('#product_description + p')
    description = description_div.text.strip() if description_div else ''
    
    # Extract category
    breadcrumb = soup.select('ul.breadcrumb li')
    category = breadcrumb[2].text.strip() if len(breadcrumb) > 2 else 'Unknown Category'
    
    # Extract rating
    rating_div = soup.select_one('p.star-rating')
    rating_class = rating_div['class'][1] if rating_div and len(rating_div['class']) > 1 else 'Zero'
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Zero': 0}
    rating = rating_map.get(rating_class, 0)
    
    # Extract image URL and download image
    image_div = soup.select_one('div.item.active img')
    image_url = ''
    image_filename = ''
    if image_div and 'src' in image_div.attrs:
        image_url = urljoin(BASE_URL, image_div['src'])
        image_filename = f"{sanitize_filename(title)}.jpg"
        save_image(image_url, image_filename)
    
    # Compile all details
    book_details = {
        'title': title,
        'price': price,
        'price_excl_tax': product_info.get('Price (excl. tax)', ''),
        'price_incl_tax': product_info.get('Price (incl. tax)', ''),
        'availability': availability,
        'description': description,
        'category': category,
        'rating': rating,
        'upc': product_info.get('UPC', ''),
        'product_type': product_info.get('Product Type', ''),
        'tax': product_info.get('Tax', ''),
        'number_of_reviews': product_info.get('Number of reviews', '0'),
        'image_url': image_url,
        'image_filename': image_filename,
        'product_url': url
    }
    
    return book_details

# Function to extract books from a category page (with pagination)
def extract_books_from_category(category):
    books = []
    page_url = category['url']
    page_num = 1
    
    while True:
        print(f"Scraping {category['name']} - Page {page_num}")
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract books on current page
        book_elements = soup.select('article.product_pod')
        for book_element in book_elements:
            book_link = book_element.select_one('h3 a')
            if book_link and 'href' in book_link.attrs:
                book_url = urljoin(page_url, book_link['href'])
                book_details = extract_book_details(book_url)
                book_details['category_name'] = category['name']
                book_details['category_slug'] = category['slug']
                books.append(book_details)
        
        # Check for next page
        next_link = soup.select_one('li.next a')
        if next_link and 'href' in next_link.attrs:
            page_url = urljoin(page_url.rsplit('/', 1)[0] + '/', next_link['href'])
            page_num += 1
        else:
            break
    
    return books

# Main function to scrape the entire website
def scrape_website():
    print("Starting to scrape Books to Scrape website...")
    
    # Extract categories
    print("Extracting categories...")
    categories = extract_categories()
    
    # Save categories to JSON
    with open('books_scraper/data/categories.json', 'w') as f:
        json.dump(categories, f, indent=4)
    
    # Extract books from each category
    all_books = []
    for category in categories:
        print(f"Extracting books from category: {category['name']}")
        category_books = extract_books_from_category(category)
        all_books.extend(category_books)
        
        # Save category books to CSV
        category_df = pd.DataFrame(category_books)
        category_df.to_csv(f"books_scraper/data/category_{category['slug']}.csv", index=False)
    
    # Save all books to CSV and JSON
    all_books_df = pd.DataFrame(all_books)
    all_books_df.to_csv('books_scraper/data/all_books.csv', index=False)
    
    with open('books_scraper/data/all_books.json', 'w') as f:
        json.dump(all_books, f, indent=4)
    
    print("Scraping completed successfully!")
    return categories, all_books

if __name__ == "__main__":
    scrape_website()
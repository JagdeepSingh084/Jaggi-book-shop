import os
from scraper import scrape_website
from generate_site import generate_site

def main():
    # Check if data already exists
    if not os.path.exists('books_scraper/data/all_books.json'):
        print("No data found. Starting scraper...")
        scrape_website()
    else:
        print("Data already exists. Skipping scraping.")
        print("To re-scrape, delete the 'books_scraper/data' directory.")
    
    # Generate static site
    generate_site()

if __name__ == "__main__":
    main()
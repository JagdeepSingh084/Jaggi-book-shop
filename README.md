# Books Scraper E-Commerce Platform

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.3.2-green)

A hybrid web application combining web scraping, static site generation, and Flask API capabilities.

## Features
- **Multi-mode Operation**
  - Static site generation (`generate_site.py`)
  - Flask REST API (`app.py`)
  - Session-based shopping cart
- **Rich Book Database**
  - 1000+ titles across 50+ categories
  - Detailed metadata including pricing, ratings, and availability
- **Modern Tech Stack**
  - Python/Flask backend
  - Jinja2 templating engine
  - RESTful API endpoints
  - Responsive CSS design

## Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/ecommerce_trae.git
cd ecommerce_trae

# Install dependencies (create requirements.txt first if needed)
pip install -r requirements.txt

# Run in development mode
flask --app books_scraper.app run --debug
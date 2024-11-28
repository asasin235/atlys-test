import requests
from bs4 import BeautifulSoup
import json
import os
import sqlite3
from src.models import Settings, Product
from src.cache import Cache

class Scraper:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.db_path = 'scraped_data.json'
        self.conn = sqlite3.connect('scraped_data.db')
        self.cache = Cache()
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products
                          (title TEXT, price REAL, image_url TEXT, image_path TEXT)''')
        self.conn.commit()

    def scrape_products(self):
        products = []
        page = 1
        max_pages = self.settings.pages if self.settings.pages else float('inf')

        while page <= max_pages:
            url = f"https://dentalstall.com/shop/page/{page}/"
            proxy = self.settings.proxy if self.settings.proxy else None

            for attempt in range(3):
                try:
                    response = requests.get(url, proxies={"http": proxy, "https": proxy} if proxy else None)
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as e:
                    if attempt == 2:
                        raise requests.exceptions.HTTPError(f"Failed to retrieve page {page}: {str(e)}")

            soup = BeautifulSoup(response.text, 'html.parser')
            product_elements = soup.find_all('div', class_='product')

            for product_element in product_elements:
                title = product_element.find('h2', class_='woocommerce-loop-product__title').text.strip()
                price = float(product_element.find('span', class_='price').text.strip().replace('₹', '').replace(',', ''))
                image_url = product_element.find('img', class_='wp-post-image')['src']
                image_path = self.download_image(image_url)

                product = Product(title=title, price=price, image_url=image_url, image_path=image_path)
                self.insert_product(product)
                products.append(product)

            page += 1

        self.save_to_json(products)
        self.notify(len(products))

    def download_image(self, url):
        response = requests.get(url)
        image_path = os.path.join('images', os.path.basename(url))
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path

    def insert_product(self, product: Product):
        cached_price = self.cache.get(product.title)
        if cached_price and float(cached_price) == product.price:
            return
        self.cache.set(product.title, product.price)
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO products (title, price, image_url, image_path)
                          VALUES (?, ?, ?, ?)''', (product.title, product.price, product.image_url, product.image_path))
        self.conn.commit()

    def save_to_json(self, products):
        with open(self.db_path, 'w') as f:
            json.dump([product.dict() for product in products], f)

    def notify(self, count):
        print(f"Scraping completed successfully. {count} products were scraped and updated in the database.")
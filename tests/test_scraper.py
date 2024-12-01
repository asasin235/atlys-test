import unittest
from unittest.mock import patch, MagicMock
from src.scraper import Scraper
from src.models import Settings, Product
from src.cache import Cache
import json
import os
import sqlite3



class TestScraper(unittest.TestCase):

    url = "https://dentalstall.com/shop/page/1/"
    def setUp(self):
        self.settings = Settings(pages=1, proxy=None)
        self.scraper = Scraper(self.settings)
        self.cache = Cache()

    def test_create_table(self):
        # Test that the table is created successfully
        self.scraper.create_table()
        cursor = self.scraper.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        self.assertTrue(cursor.fetchone())

    @patch('src.scraper.BeautifulSoup')
    def test_retrieve_page_elements(self, mock_bs):
        # Test that the page elements are retrieved successfully
        mock_bs.return_value.find_all.return_value = [MagicMock()]
        elements = self.scraper.retrieve_page_elements(self.url, None, 1)
        self.assertTrue(elements)

    @patch('src.scraper.BeautifulSoup')
    def test_retrieve_page_elements_failure(self, mock_bs):
        # Test that an exception is raised when page elements cannot be retrieved
        mock_bs.return_value.find_all.return_value = []
        with self.assertRaises(Exception):
            self.scraper.retrieve_page_elements('invalidURL', None, 1)

    def test_extract_product(self):
        # Create mock elements
        product_element = MagicMock()
        title_element = MagicMock()
        title_element.text.strip.return_value = 'Product Title'
        price_element = MagicMock()
        price_element.text.strip.return_value = '₹100'
        image_element = MagicMock()
        image_element.__getitem__.return_value = 'https://example.com/image.jpg'

        # Set the side effects for the find method
        product_element.find.side_effect = [title_element, price_element, image_element]

        # Call the method
        product = self.scraper.extract_product(product_element)

        # Assert the product is correctly extracted
        self.assertIsNotNone(product)
        self.assertEqual(product.title, 'Product Title')
        self.assertEqual(product.price, 100.0)  # Assuming convert_price('₹100') returns 100.0
        self.assertEqual(product.image_url, 'https://example.com/image.jpg')

    def test_extract_product_invalid(self):
        # Create mock elements with missing title
        product_element = MagicMock()
        product_element.find.side_effect = [None, None, None]

        # Call the method
        product = self.scraper.extract_product(product_element)

        # Assert the product is None
        self.assertIsNone(product)

    @patch('src.scraper.requests.get')
    def test_download_image(self, mock_get):
        # Test that an image is downloaded successfully
        mock_get.return_value.content = b'content'
        image_url = 'https://example.com/image.jpg'
        image_path = self.scraper.download_image(image_url)
        self.assertTrue(os.path.exists(image_path))

    def test_insert_product(self):
        # Test that a product is inserted into the database successfully
        product = Product(title='title', price=10.99, image_url='image_url', image_path='image_path')
        self.scraper.insert_product(product)
        cursor = self.scraper.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE title='title'")
        self.assertTrue(cursor.fetchone())

    def test_save_to_json(self):
        # Test that products are saved to a JSON file successfully
        products = [Product(title='title', price=10.99, image_url='image_url', image_path='image_path')]
        self.scraper.save_to_json(products)
        with open(self.scraper.db_path, 'r') as f:
            data = json.load(f)
            self.assertTrue(data)

    def tearDown(self):
        # Close the database connection and remove the JSON file
        self.scraper.conn.close()
        if os.path.exists(self.scraper.db_path):
            os.remove(self.scraper.db_path)
        if os.path.exists('images'):
            for file in os.listdir('images'):
                os.remove(os.path.join('images', file))
            os.rmdir('images')

if __name__ == '__main__':
    unittest.main()
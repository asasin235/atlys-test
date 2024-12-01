# Scraper Project

This project is a web scraper that extracts product information from a specified website and stores the data in a SQLite database and a JSON file. The scraper uses Selenium for web automation and BeautifulSoup for parsing HTML content.

## Features

- Scrapes product information including title, price, and image URL.
- Downloads product images.
- Stores product data in a SQLite database.
- Saves product data to a JSON file.
- Supports proxy configuration.
- Logs warnings for missing elements.

## Requirements

- Python 3.7+
- `requests`
- `beautifulsoup4`
- `selenium`
- `sqlite3`
- `unittest`
- `unittest.mock`
- `json`
- `os`
- `logging`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/scraper-project.git
    cd scraper-project
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Download the ChromeDriver and ensure it is in your PATH:
    ```sh
    # Example for macOS
    brew install chromedriver
    ```

## Usage

1. Configure the settings in `src/models.py`:
    ```python
    class Settings:
        def __init__(self, pages=1, proxy=None):
            self.pages = pages
            self.proxy = proxy
    ```

2. Run the scraper:
    ```sh
    python src/scraper.py
    ```

3. The scraped data will be stored in `scraped_data.db` and `scraped_data.json`.

## Testing

1. Run the tests using `unittest`:
    ```sh
    python -m unittest discover tests
    ```

## Project Structure

```
scraper-project/
├── src/
│   ├── scraper.py
│   ├── models.py
│   ├── cache.py
│   ├── utils.py
│   └── logging_config.py
├── tests/
│   ├── test_scraper.py
│   └── test_main.http
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
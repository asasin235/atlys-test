# Scraper Project

This project is a web scraper that extracts product information from a specified website and stores the data in a SQLite database and a JSON file. The scraper uses Selenium for web automation and BeautifulSoup for parsing HTML content.

## Features
- Used selenium as a web automation tool because the page was lazy loaded
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
- `json`
- `os`
- `logging`
## Postman Curls
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/23117922-34380fb6-23d9-41b4-a7ab-a4784cce4fd8?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D23117922-34380fb6-23d9-41b4-a7ab-a4784cce4fd8%26entityType%3Dcollection%26workspaceId%3Dbfa5b207-2c60-4a90-b59d-fb4e1a2cab23#?env%5BNew%20Environment%5D=W3sia2V5IjoiYXV0aCIsInZhbHVlIjoiIiwidHlwZSI6ImRlZmF1bHQiLCJlbmFibGVkIjp0cnVlLCJzZXNzaW9uVmFsdWUiOiJCZWFyZXIgeW91cl9zdGF0aWNfdG9rZW4iLCJjb21wbGV0ZVNlc3Npb25WYWx1ZSI6IkJlYXJlciB5b3VyX3N0YXRpY190b2tlbiIsInNlc3Npb25JbmRleCI6MH1d)
## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/asasin235/scraper-project.git
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

Made by Aatif Rashid For 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from utils import load_config  # Importing paths dictionary from utils.py

# Base URL
BASE_URL = "https://stockanalysis.com/stocks/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

paths = load_config()
CSV_PATH = os.path.join(paths["data_processed"], "stocks.csv")

def get_stock_data():
    all_stocks = []
    page_number = 1  # Start from page 1
    next_page = BASE_URL  # Start with the main URL

    while next_page:
        print(f"Scraping page {page_number}...")

        # Request the page
        response = requests.get(next_page, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the stock table
        table = soup.find("table")
        if not table:
            print(f"No stock table found on page {page_number}")
            break

        # Extract stock symbols and names
        rows = table.find_all("tr")[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 2:
                continue
            symbol = cols[0].text.strip()
            name = cols[1].text.strip()
            all_stocks.append((symbol, name))

        # Find "Next" button link (Fixed for BeautifulSoup 4.11+)
        next_button = soup.find("a", string="Next")  # Replaced 'text' with 'string'
        if next_button:
            next_page = "https://stockanalysis.com" + next_button["href"]
            page_number += 1
        else:
            print("No more pages to scrape.")
            break

    return all_stocks

def save_to_csv(data):
    df = pd.DataFrame(data, columns=["Symbol", "Company Name"])
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"Saved {len(data)} stocks to {CSV_PATH}")

if __name__ == "__main__":
    stocks = get_stock_data()
    if stocks:
        save_to_csv(stocks)

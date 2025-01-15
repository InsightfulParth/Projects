import requests
from bs4 import BeautifulSoup

# ScraperAPI proxy URL (replace with your API key)
scraper_api_url = "http://api.scraperapi.com/"
api_key = "your_api_key_here"  # Replace with your ScraperAPI key

# Define headers to mimic a browser request (important for bypassing bot detection)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

# URL to fetch data from
url = "https://www.nseindia.com/"

# Add ScraperAPI parameters
params = {
    "api_key": api_key,
    "url": url,
}

try:
    # Fetch the page content using ScraperAPI
    response = requests.get(scraper_api_url, headers=headers, params=params, timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the desired table (adjust based on the website's structure)
    tables = soup.find_all("table")  # Finds all table elements
    
    if tables:
        for i, table in enumerate(tables, 1):
            print(f"Table {i}:")
            rows = table.find_all("tr")
            for row in rows:
                cols = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]
                print(cols)
            print("\n")
    else:
        print("No tables found on the page.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the data: {e}")

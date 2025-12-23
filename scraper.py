import requests
from bs4 import BeautifulSoup

def scrape_text(url):
    """
    Scrapes the text content from a given URL.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"Error scraping URL: {e}")
        return ""

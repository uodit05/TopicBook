import requests
from bs4 import BeautifulSoup

def scrape_website(url: str) -> str:
    """
    Scrapes the text content from a given URL.
    """
    print(f"-> Scraping {url}...")
    try:
        # Set a User-Agent header to mimic a real browser visit
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all paragraph tags and join their text. This is a simple heuristic
        # that works for many articles and blogs.
        paragraphs = soup.find_all('p')
        text_content = ' '.join([p.get_text() for p in paragraphs])
        
        return text_content

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return "" # Return empty string on failure
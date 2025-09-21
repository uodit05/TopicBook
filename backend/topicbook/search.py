import os
import requests
from dotenv import load_dotenv

def search_google(query: str, num_results: int = 10) -> list[str]:
    """
    Searches Google for a given query and returns a list of URLs.
    """
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    
    if not api_key or not search_engine_id:
        raise ValueError("API key or Search Engine ID not found in .env file")

    # The API endpoint for Google Custom Search
    url = "https://www.googleapis.com/customsearch/v1"
    
    # Parameters for the API request
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'num': num_results
    }
    
    print("-> Searching Google for relevant links...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
        
        search_results = response.json()
        
        # Extract the links from the search results
        urls = [item['link'] for item in search_results.get('items', [])]
        
        print(f"-> Found {len(urls)} links.")
        return urls

    except requests.exceptions.RequestException as e:
        print(f"Error making request to Google Search API: {e}")
        return []

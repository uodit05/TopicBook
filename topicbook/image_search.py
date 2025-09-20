# topicbook/image_search.py

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

def find_image_for_query(query: str) -> str | None:
    """
    Performs a Google Image Search for a query and returns the URL of the top result.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")

    if not api_key or not search_engine_id:
        raise ValueError("API key or Search Engine ID not found in .env file")

    try:
        # Build the custom search service
        service = build("customsearch", "v1", developerKey=api_key)
        
        # Execute the search
        result = service.cse().list(
            q=query,
            cx=search_engine_id,
            searchType='image',  # Specify that we are searching for images
            num=1                # We only want the top result
        ).execute()

        # Extract the image URL from the result
        if 'items' in result and len(result['items']) > 0:
            top_image_url = result['items'][0]['link']
            return top_image_url
        else:
            return None # Return None if no images are found

    except Exception as e:
        print(f"   - An error occurred during image search for '{query}': {e}")
        return None
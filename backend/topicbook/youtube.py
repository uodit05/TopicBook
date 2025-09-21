import os
import time
from dotenv import load_dotenv
from googleapiclient.discovery import build
import requests

def search_youtube_and_get_transcripts(query: str, max_results: int = 5):
    """
    Searches YouTube for videos and then uses a third-party API
    to get their transcripts.
    """
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise ValueError("YOUTUBE_API_KEY not found in .env file")

    print("\n-> Searching YouTube for videos...")
    
    youtube = build('youtube', 'v3', developerKey=api_key)

    search_request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results,
        type='video'
    )
    search_response = search_request.execute()

    video_data = [
        {"id": item['id']['videoId'], "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"} 
        for item in search_response.get('items', [])
    ]
    
    if not video_data:
        print("-> No videos found on YouTube.")
        return "", []
    
    print(f"-> Found {len(video_data)} videos. Fetching transcripts via API...")
    
    all_transcripts = ""
    processed_urls = []
    
    for video in video_data:
        try:
            api_url = f"https://www.youtubevideotranscripts.com/api/transcript?videoId={video['id']}"
            
            response = requests.get(api_url)
            response.raise_for_status()
            
            data = response.json()
            snippets = [item['text'] for item in data.get('transcript', [])]
            transcript_text = ' '.join(snippets)
            
            if transcript_text:
                all_transcripts += transcript_text + "\n\n"
                processed_urls.append(video['url'])
                print(f"   - Success: Transcript for video ID {video['id']} added.")
            else:
                print(f"   - API response for video ID {video['id']} was empty.")

        except Exception as e:
            print(f"   - An error occurred while fetching transcript for video ID {video['id']}: {e}")
            continue
        finally:
            # Added a 2-second delay to be respectful to the API
            time.sleep(2)
            
    return all_transcripts, processed_urls
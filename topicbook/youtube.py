import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

def search_youtube_and_get_transcripts(query: str, max_results: int = 5) -> str:
    """
    Searches YouTube for videos and fetches their transcripts, including regional English variants.
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
        type='video',
        videoCaption='closedCaption'
    )
    search_response = search_request.execute()

    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
    
    if not video_ids:
        print("-> No videos with captions found on YouTube.")
        return ""
    
    print(f"-> Found {len(video_ids)} videos. Fetching transcripts...")
    
    all_transcripts = ""
    ytt_api = YouTubeTranscriptApi() 

    preferred_languages = ['en', 'en-IN', 'en-US', 'en-GB', 'en-AU', 'en-CA']

    for video_id in video_ids:
        try:
            # Try to fetch transcript with preferred languages
            fetched_transcript_obj = ytt_api.fetch(video_id, languages=preferred_languages)
            
            transcript_text = ' '.join([item.text for item in fetched_transcript_obj])
            all_transcripts += transcript_text + "\n\n"
        except Exception as e:
            print(f"   - Could not fetch transcript for video ID {video_id}. Reason: {e}")
            continue
            
    return all_transcripts
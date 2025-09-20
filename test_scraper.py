# test_scraper.py
import requests

# A known YouTube video ID to test with
VIDEO_ID = "kqtD5dpn9C8"

# The new API URL you discovered
API_URL = f"https://www.youtubevideotranscripts.com/api/transcript?videoId={VIDEO_ID}"

print(f"--- Testing transcript API endpoint ---")
print(f"Targeting URL: {API_URL}")

try:
    # Make a request to the API
    response = requests.get(API_URL)
    response.raise_for_status() # Check for any request errors
    
    # Parse the JSON response
    data = response.json()
    
    # Extract the text from each snippet in the 'transcript' list
    transcript_snippets = [item['text'] for item in data.get('transcript', [])]
    transcript_text = ' '.join(transcript_snippets)
    
    if transcript_text:
        print("\n✅ SUCCESS! Fetched and parsed transcript from API.")
        print("\n--- Transcript Snippet ---")
        print(transcript_text[:300] + "...")
    else:
        print("\n❌ FAILURE! The JSON response did not contain a valid transcript.")

except Exception as e:
    print(f"\n❌ FAILURE! An error occurred during the API request.")
    print(f"   Error details: {e}")

print("\n--- Test complete ---")
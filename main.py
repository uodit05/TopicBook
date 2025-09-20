import argparse
from topicbook.search import search_google

def main():
    """
    Main function to run the TopicBook generation process.
    """
    parser = argparse.ArgumentParser(description="Generate a TopicBook for a given topic.")
    parser.add_argument("topic", type=str, help="The topic you want to learn about.")
    
    args = parser.parse_args()
    topic = args.topic
    
    print(f"🚀 Starting TopicBook generation for: '{topic}'")
    
    # 1. Search for content
    urls = search_google(query=topic)
    
    if not urls:
        print("Could not find any relevant links. Exiting.")
        return
        
    print("\nHere are the links we found:")
    for url in urls:
        print(f"- {url}")

    # --- Future logic will go here ---
    # 2. Scrape content
    # 3. Structure with AI
    # 4. Curate with AI
    # 5. Generate Markdown file

if __name__ == "__main__":
    main()
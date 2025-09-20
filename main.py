import argparse
from topicbook.search import search_google
from topicbook.scraper import scrape_website

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
        
    # 2. Scrape content from each URL
    all_text_content = ""
    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] Scraping URL: {url}")
        content = scrape_website(url)
        if content:
            all_text_content += content + "\n\n"
            print(f"-> Successfully scraped and added content.")
        else:
            print(f"-> Failed to scrape content.")

    print(f"\n✅ Total text content scraped: {len(all_text_content)} characters.")

    # --- Future logic will go here ---
    # 3. Structure with AI
    # 4. Curate with AI
    # 5. Generate Markdown file

if __name__ == "__main__":
    main()
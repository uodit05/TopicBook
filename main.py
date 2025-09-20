import argparse
from topicbook.search import search_google
from topicbook.scraper import scrape_website
from topicbook.ai import generate_structure

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
            print("-> Successfully scraped and added content.")
        else:
            print("-> Failed to scrape content.")
            
    print(f"\n✅ Total text content scraped: {len(all_text_content)} characters.")

    # 3. Structure with AI
    structure = generate_structure(topic, all_text_content)
    
    if not structure:
        print("Could not generate a structure with the AI. Exiting.")
        return
        
    print("\n--- Generated TopicBook Structure ---")
    print(structure)
    print("------------------------------------")

    # --- Future logic will go here ---
    # 4. Curate with AI
    # 5. Generate Markdown file

if __name__ == "__main__":
    main()
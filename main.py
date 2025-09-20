import argparse
import re
import os

from topicbook.search import search_google
from topicbook.scraper import scrape_website
from topicbook.ai import generate_structure, generate_final_topicbook

def main():
    """
    Main function to run the TopicBook generation process.
    """
    parser = argparse.ArgumentParser(description="Generate a TopicBook for a given topic.")
    parser.add_argument("topic", type=str, help="The topic you want to learn about.")
    args = parser.parse_args()
    topic = args.topic
    
    print(f"🚀 Starting TopicBook generation for: '{topic}'")
    
    # 1. Search
    urls = search_google(query=topic)
    if not urls:
        print("Could not find any relevant links. Exiting.")
        return
        
    # 2. Scrape
    all_text_content = ""
    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] Scraping URL: {url}")
        content = scrape_website(url)
        if content:
            all_text_content += content + "\n\n"
            
    print(f"\n✅ Total text content scraped: {len(all_text_content)} characters.")

    # 3. Structure with AI
    structure = generate_structure(topic, all_text_content)
    if not structure:
        print("Could not generate a structure with the AI. Exiting.")
        return
        
    print("\n--- Generated TopicBook Structure ---")
    print(structure)
    print("------------------------------------")

    # 4. Generate the final book content using the structure
    final_content = generate_final_topicbook(topic, structure, all_text_content)
    if not final_content:
        print("Could not generate the final content with the AI. Exiting.")
        return

    # 5. Save the final book to a file
    output_dir = "Generated-Books"
    os.makedirs(output_dir, exist_ok=True)
    base_filename = re.sub(r'[\\/*?:"<>|]', "", topic).replace(" ", "_")
    counter = 1
    output_filename = f"{base_filename}.md"
    file_path = os.path.join(output_dir, output_filename)

    while os.path.exists(file_path):
        output_filename = f"{base_filename}_{counter}.md"
        file_path = os.path.join(output_dir, output_filename)
        counter += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"\n🎉 Success! Your TopicBook has been generated: {file_path}")

if __name__ == "__main__":
    main()
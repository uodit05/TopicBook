import argparse
import re
import os
import json 

from topicbook.search import search_google
from topicbook.scraper import scrape_website
from topicbook.youtube import search_youtube_and_get_transcripts
from topicbook.image_search import find_image_for_query 
from topicbook.ai import generate_structure, generate_final_topicbook


def main():
    parser = argparse.ArgumentParser(description="Generate a TopicBook for a given topic.")
    parser.add_argument("topic", type=str, help="The topic you want to learn about.")
    args = parser.parse_args()
    topic = args.topic
    
    print(f"🚀 Starting TopicBook generation for: '{topic}'")
    
    # 1 & 2. Search and Scrape Web & YouTube
    source_data = []
    urls = search_google(query=topic)
    if urls:
        for i, url in enumerate(urls):
            print(f"\n[{i+1}/{len(urls)}] Scraping URL: {url}")
            content = scrape_website(url)
            if content:
                source_data.append({"url": url, "content": content})

    transcript_content, transcript_urls = search_youtube_and_get_transcripts(query=topic)
    # Add each transcript as its own source
    if transcript_urls:
        # Assuming one block of text for all for now, but associating with all URLs
        # A more advanced version could split this
        combined_transcript_content = " ".join(transcript_content.split())
        source_data.append({"url": ", ".join(transcript_urls), "content": combined_transcript_content})

    if not source_data:
        print("Could not gather any content. Exiting.")
        return
    
    # NEW: Format source data as a clearly labeled string for the AI
    source_text_for_ai = ""
    for i, source in enumerate(source_data):
        source_text_for_ai += f"[SOURCE {i+1}]: URL = {source['url']}\n"
        source_text_for_ai += f"CONTENT: {source['content']}\n\n"
            
    print(f"\n✅ Total text content gathered.")

    # 3. Structure with AI
    structure = generate_structure(topic, source_text_for_ai)
    if not structure:
        print("Could not generate a structure. Exiting.")
        return
        
    print("\n--- Generated TopicBook Structure --- \n" + structure)

    # 4. Image Search
    print("\n-> Searching for relevant images for each section...")
    section_titles = [line for line in structure.split('\n') if line.strip().startswith('#')]
    image_map = {}
    for title in section_titles:
        clean_title = re.sub(r'^\W*\d+\.?\d*\s*', '', title).strip()
        if len(clean_title) > 5:
             image_url = find_image_for_query(f"{clean_title} diagram illustration")
             if image_url:
                 image_map[title] = image_url
                 print(f"   - Found image for: {clean_title}")

    # 5. Generate the final book content
    final_content = generate_final_topicbook(topic, structure, source_text_for_ai, image_map)
    if not final_content:
        print("Could not generate the final content. Exiting.")
        return

    # 6. Save the final book to a file
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
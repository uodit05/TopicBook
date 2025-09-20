import argparse
import re
import os

from topicbook.search import search_google
from topicbook.scraper import scrape_website
from topicbook.youtube import search_youtube_and_get_transcripts
from topicbook.image_search import find_image_for_query
from topicbook.ai import plan_research_queries, generate_structure, generate_final_topicbook

def main():
    parser = argparse.ArgumentParser(description="Generate a personalized TopicBook.")
    parser.add_argument("topic", type=str, help="The main topic you want to learn about.")
    parser.add_argument("-d", "--description", type=str, help="A detailed description of your needs and background.")
    args = parser.parse_args()
    topic = args.topic
    description = args.description
    
    print(f"🚀 Starting TopicBook generation for: '{topic}'")
    if description:
        print(f"   User context: '{description}'")

    # 1. Plan Research with AI
    search_queries = plan_research_queries(topic, description)
    if not search_queries:
        print("Could not generate search plan. Exiting.")
        return

    # 2. Execute Research Plan (Gather Data)
    source_data = []
    for query in search_queries:
        print(f"\n--- Executing search: \"{query}\" ---")
        
        # Search and scrape web pages
        urls = search_google(query=query, num_results=3) # Limit to 3 results per query
        if urls:
            for i, url in enumerate(urls):
                print(f"-> Scraping URL: {url}")
                content = scrape_website(url)
                if content:
                    source_data.append({"url": url, "content": content})

        # Search and scrape YouTube transcripts
        transcript_content, transcript_urls = search_youtube_and_get_transcripts(query=query, max_results=2) # Limit to 2 videos
        if transcript_urls:
            combined_transcript_content = " ".join(transcript_content.split())
            source_data.append({"url": ", ".join(transcript_urls), "content": combined_transcript_content})

    if not source_data:
        print("Could not gather any content. Exiting.")
        return

    source_text_for_ai = ""
    for i, source in enumerate(source_data):
        source_text_for_ai += f"[SOURCE {i+1}]: URL = {source['url']}\nCONTENT: {source['content']}\n\n"
            
    print(f"\n✅ Total research content gathered.")

    # 3. Structure with AI (now with description)
    structure = generate_structure(topic, description, source_text_for_ai)
    if not structure:
        print("Could not generate a structure. Exiting.")
        return
    print("\n--- Generated Personalized Structure --- \n" + structure)

    # 4. Image Search
    print("\n-> Searching for relevant images...")
    section_titles = [line for line in structure.split('\n') if line.strip().startswith('#')]
    image_map = {}
    for title in section_titles:
        clean_title = re.sub(r'^\W*\d+\.?\d*\s*', '', title).strip()
        if len(clean_title) > 5:
             image_url = find_image_for_query(f"{clean_title} diagram illustration")
             if image_url:
                 image_map[title] = image_url
                 print(f"   - Found image for: {clean_title}")

    # 5. Generate Final Book (now with description)
    final_content = generate_final_topicbook(topic, description, structure, source_text_for_ai, image_map)
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
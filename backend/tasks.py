import re
import os
import json
from celery import Celery

from topicbook.search import search_google
from topicbook.scraper import scrape_website
from topicbook.youtube import search_youtube_and_get_transcripts
from topicbook.image_search import find_image_for_query
from topicbook.ai import plan_research_queries, generate_structure, generate_final_topicbook, generate_image_search_query

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task(bind=True)
def generate_topicbook_task(self, topic: str, description: str | None):
    """
    The main Celery task that runs the entire TopicBook generation pipeline.
    """
    def update_status(message):
        print(message)
        self.update_state(state='PROGRESS', meta={'status': message})

    # steps 1, 2, and 3 for Research and Structuring
    update_status(f"🚀 Starting TopicBook generation for: '{topic}'")
    if description:
        update_status(f"   User context: '{description}'")

    search_queries = plan_research_queries(topic, description)
    
    source_data = []
    for query in search_queries:
        update_status(f"\n--- Executing search: \"{query}\" ---")
        urls = search_google(query=query, num_results=5)
        if urls:
            for url in urls:
                update_status(f"-> Scraping URL: {url}")
                content = scrape_website(url)
                if content:
                    source_data.append({"url": url, "content": content})
        
        transcript_content, transcript_urls = search_youtube_and_get_transcripts(query=query, max_results=3)
        if transcript_urls:
            source_data.append({"url": ", ".join(transcript_urls), "content": transcript_content})

    if not source_data:
        update_status("Could not gather any content. Exiting.")
        return {"status": "FAILURE", "error": "Could not gather any content."}

    source_text_for_ai = ""
    for i, source in enumerate(source_data):
        source_text_for_ai += f"[SOURCE {i+1}]: URL = {source['url']}\nCONTENT: {source['content']}\n\n"
    update_status("✅ Total research content gathered.")

    structure = generate_structure(topic, description, source_text_for_ai)
    if not structure:
        update_status("Could not generate a structure. Exiting.")
        return {"status": "FAILURE", "error": "Could not generate structure."}
    update_status("--- Generated Personalized Structure --- \n" + structure)

    # 4. AI-Powered Image Search 
    update_status("-> Planning and searching for relevant images...")
    section_titles = [line for line in structure.split('\n') if line.strip().startswith('#')]
    image_map = {}
    for title in section_titles:
        clean_title = re.sub(r'^\W*\d+\.?\d*\s*', '', title).strip()
        if len(clean_title) > 5:
            # Step 4a: AI generates a better search query
            image_query = generate_image_search_query(topic, title)
            update_status(f"   - AI generated image query: '{image_query}'")
             
            # Step 4b: Execute the smarter search
            image_url = find_image_for_query(image_query)
            if image_url:
                image_map[title] = image_url
                update_status(f"   - Found image for: {clean_title}")

    # 5. Generate Final Book
    final_content = generate_final_topicbook(topic, description, structure, source_text_for_ai, image_map)
    if not final_content:
        update_status("Could not generate the final content. Exiting.")
        return {"status": "FAILURE", "error": "Could not generate final content."}

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
    
    final_message = f"🎉 Success! Your TopicBook has been generated: {file_path}"
    update_status(final_message)
    return {"status": "SUCCESS", "result": final_message, "filepath": file_path}
import os
import google.generativeai as genai
from dotenv import load_dotenv

def generate_structure(topic: str, text_content: str) -> str:
    """
    Uses the Gemini API to generate a structured outline from a block of text.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    prompt = f"""
    Act as an expert instructional designer. You have been given a large amount of unstructured text
    scraped from various web pages about the topic: "{topic}".

    Your task is to analyze all of the text and create a comprehensive, logical, and easy-to-follow
    table of contents for a guide that will teach this topic to a beginner.

    The output should be ONLY the table of contents in Markdown format, with nested sub-topics.
    Start with an introduction and end with a conclusion.
    Do not include any other text, greetings, or explanations.

    Here is the raw text:
    ---
    {text_content}
    ---
    """
    
    print("\n-> Generating structure with AI. This may take a moment...")

    try:
        response = model.generate_content(prompt)
        print("-> AI structure generated successfully.")
        return response.text
    except Exception as e:
        print(f"An error occurred while communicating with the Gemini API: {e}")
        return ""


def generate_final_topicbook(topic: str, structure: str, text_content: str, image_map: dict) -> str:
    """
    Uses the Gemini API to write the full content of the TopicBook, with curated links and images.
    """
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    image_instructions = "\n".join([f"- For section '{title}', use image URL: {url}" for title, url in image_map.items()])

    prompt = f"""
    You are an expert author and educator. Your task is to write a complete, in-depth guide
    on the topic of "{topic}". You must follow the provided Markdown outline exactly. Use the provided
    raw source text to write the content.

    **CRITICAL INSTRUCTIONS FOR LINKS AND CITATIONS:**
    1.  Your primary goal is to synthesize the information into a seamless guide. You DO NOT need to cite every fact.
    2.  However, if you find that a specific source (e.g., [SOURCE 1], [SOURCE 2], etc.) contains exceptionally valuable information for a deep-dive, you should add a "further reading" link.
    3.  When you add a link, you MUST use the real URL provided for that source.
    4.  The hyperlink MUST be formatted correctly in Markdown. For example:
        "*(For a deeper dive on this, see: [Title of Article](URL_FROM_THE_SOURCE_LIST))*."
    
    **CRITICAL INSTRUCTIONS FOR IMAGES:**
    1.  When you write a section that has a corresponding image URL, you MUST embed that image using Markdown syntax: `![Generated alt text](image_url_here)`. Generate a concise and relevant alt text.

    ---
    HERE IS THE EXACT MARKDOWN OUTLINE YOU MUST FOLLOW:
    {structure}
    ---
    HERE IS THE RAW SOURCE TEXT. EACH SOURCE IS CLEARLY LABELED (e.g., [SOURCE 1]):
    {text_content} 
    ---
    HERE ARE THE IMAGE URLS TO USE FOR SPECIFIC SECTIONS:
    {image_instructions}
    ---
    """
    print("\n-> Writing the full TopicBook with AI, including images and real links...")

    try:
        response = model.generate_content(prompt)
        print("-> TopicBook content generated successfully.")
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while generating the final content: {e}")
        return ""
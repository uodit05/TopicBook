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

def generate_final_topicbook(topic: str, structure: str, text_content: str) -> str:
    """
    Uses the Gemini API to write the full content of the TopicBook based on the generated structure.
    """

    model = genai.GenerativeModel('gemini-2.5-flash-lite') 

    prompt = f"""
    You are an expert author and educator. Your task is to write a complete, in-depth guide
    on the topic of "{topic}".

    You have been provided with raw source text and a precise Markdown outline. Your job is to
    flesh out every single section and sub-section from the outline with detailed, high-quality,
    and beginner-friendly content, using ONLY the provided raw text as your source of information.

    The final output must be a single, cohesive Markdown document that exactly follows the
    provided structure.

    ---
    HERE IS THE EXACT MARKDOWN OUTLINE YOU MUST FOLLOW:
    {structure}
    ---
    HERE IS THE RAW SOURCE TEXT YOU MUST USE:
    {text_content}
    ---
    """

    print("\n-> Writing the full TopicBook with AI. This is the final step and may take some time...")

    try:
        response = model.generate_content(prompt)
        print("-> TopicBook content generated successfully.")
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while generating the final content: {e}")
        return ""
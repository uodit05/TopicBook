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
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    # This is the prompt engineering part. We give the AI a role, context, and a specific task.
    prompt = f"""
    Act as an expert instructional designer. You have been given a large amount of unstructured text
    scraped from various web pages about the topic: "{topic}".

    Your task is to analyze all of the text and create a comprehensive, logical, and easy-to-follow
    table of contents for a guide that will teach this topic to a beginner.

    The output should be ONLY the table of contents in Markdown format.
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
    
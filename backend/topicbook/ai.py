import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

def plan_research_queries(topic: str, description: str | None) -> list[str]:
    """
    Uses an LLM to generate a list of targeted search queries.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    prompt = f"""
    You are a research assistant. Your goal is to generate a list of 3-5 highly targeted Google search queries
    that will find the best information for a user's request.

    The user wants to learn about: "{topic}"
    Here is their specific description and background: "{description if description else 'No description provided.'}"

    Based on this, generate a list of 3-5 concise search queries.
    The output should be ONLY a Python-style list of strings. For example: ["query 1", "query 2", "query 3"]
    """

    print("-> Planning research queries with AI...")
    try:
        response = model.generate_content(prompt)
        # Use regex to find all strings within quotes
        queries = re.findall(r'"(.*?)"', response.text)
        print(f"-> Generated queries: {queries}")
        # Fallback in case regex fails
        if not queries:
            return [topic]
        return queries
    except Exception as e:
        print(f"   - Could not generate search plan. Defaulting to topic. Error: {e}")
        return [topic]


def generate_structure(topic: str, description: str | None, text_content: str) -> str:
    """
    Uses the Gemini API to generate a personalized structured outline.
    """
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    prompt = f"""
    Act as an expert instructional designer creating a personalized learning plan.
    The user wants to learn about: "{topic}"
    Their background and specific request is: "{description if description else 'A general overview.'}"

    Based on the user's request and the provided source text, create a comprehensive, logical table of contents.
    Tailor the structure to the user's needs (e.g., focus on implementation if they are a developer, 
    or on theory if they ask for math).

    The output should be ONLY the table of contents in Markdown format.
    
    Here is the raw source text:
    ---
    {text_content}
    ---
    """
    
    print("\n-> Generating personalized structure with AI...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


def generate_final_topicbook(topic: str, description: str | None, structure: str, text_content: str, image_map: dict) -> str:
    """
    Uses the Gemini API to write the full TopicBook, tailored to the user's description.
    """
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    image_instructions = "\n".join([f"- For section '{title}', use image URL: {url}" for title, url in image_map.items()])

    prompt = f"""
    You are an expert author writing a personalized notes-taking book guide for a user.
    The topic is: "{topic}"
    The user has described that his specific background and request is for the specific topic is: "{description if description else 'A general overview.'}"

    Your task is to write a complete, in-depth guide following the provided Markdown outline.
    Use the provided source text. Most importantly, **tailor your language, examples, and analogies
    to the user's described background and goals.** For example, if they are a biologist, use biological analogies.
    If they want code, provide code snippets, if they want math realated, explain in-depth with math, if they need research related, explain in-depth of everythin.

    CRITICAL INSTRUCTIONS (Links, Images, etc.):
    1.  Follow the provided outline exactly.
    2.  If a source URL contains exceptionally valuable information for a deep-dive, add a "further reading" link like: "*(For a deeper dive, see: [Article Title](URL))*". You MUST use the real URL from the source list.
    3.  Embed provided images using Markdown: `![Generated alt text](image_url_here)`.

    ---
    HERE IS THE EXACT MARKDOWN OUTLINE TO FOLLOW:
    {structure}
    ---
    HERE IS THE RAW SOURCE TEXT (EACH SOURCE IS LABELED):
    {text_content} 
    ---
    HERE ARE THE IMAGE URLS FOR SPECIFIC SECTIONS:
    {image_instructions}
    ---
    """

    print("\n-> Writing the full personalized TopicBook with AI...")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    
def generate_image_search_query(topic: str, section_title: str) -> str:
    """
    Uses an LLM to generate a highly descriptive image search query.
    """
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # Clean the section title to remove markdown hashes and numbers
    clean_title = re.sub(r'^\W*\d+\.?\d*\s*', '', section_title).strip()

    prompt = f"""
    You are a research assistant. Your task is to generate one, single, highly descriptive Google Image search query
    to find the best possible diagram, illustration, or photo for the sub-topic: "{clean_title}"
    within the main topic of "{topic}".

    The query should be optimized to find educational and clear images.
    Return ONLY the single search query string and nothing else. Do not add quotes.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"   - Could not generate image query. Defaulting to section title. Error: {e}")
        return f"{clean_title} diagram illustration"
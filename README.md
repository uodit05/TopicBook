# TopicBook  

An intelligent, AI-powered learning assistant that generates personalized, media-rich learning guides on any topic.


---
## About The Project

TopicBook was designed to solve the problem of information overload when trying to learn a new subject. Instead of just getting a list of links, TopicBook acts as an AI research agent. It intelligently plans its research, gathers information from multiple sources like articles and videos, creates a logical structure, and then authors a complete, personalized guide tailored to your specific needs and background.

The result is a deeply researched, easy-to-read document complete with images, examples, analogies, and links for further reading.

---
## ✨ Features

* **Personalized Input:** Provide a topic and a detailed description of your learning goals and background for a truly curated experience.
* **AI Research Planning:** An LLM first generates a list of targeted search queries to find the most relevant information.
* **Multi-Source Data Gathering:** The agent scrapes content from both Google Search results and YouTube video transcripts.
* **Intelligent Structuring:** The AI analyzes all gathered text to create a comprehensive and logical table of contents (the "blueprint").
* **AI-Powered Image Search:** For each major section, the agent generates a descriptive query to find the most relevant diagrams and illustrations.
* **Rich Content Authoring:** The final book is written by an LLM, which follows the blueprint, embeds images, and intelligently adds "Further Reading" hyperlinks to the best sources.
* **Real-time Log Streaming:** Watch the agent work in real-time through a live log that streams directly to the user interface.
* **Sidebar Book Viewer:** All generated books are listed in a clean sidebar, allowing you to open and read them in a pop-up modal.

---
## 🛠️ Tech Stack

The project is a full-stack application built with a modern technology stack.

* **Backend:**
    * Python
    * FastAPI (Web Framework)
    * Celery (Asynchronous Task Queue)
    * Redis (Message Broker)
    * Google AI (for Gemini models)

* **Frontend:**
    * React
    * TypeScript
    * Vite (Build Tool)
    * Tailwind CSS (Styling)
    * shadcn/ui (Component Library)
    * Framer Motion (Animations)

---
## 🏁 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

You must have the following software installed on your machine:
* **Python** (v3.11+ recommended, preferably managed with `pyenv`)
* **Node.js** (LTS version recommended, preferably managed with `nvm`)
* **Redis**
    * On Debian/Ubuntu: `sudo apt-get install redis-server`
* **Git**

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/uodit05/TopicBook.git
    cd TopicBook
    ```

2.  **Set up Backend:**
    ```sh
    # Navigate to the backend directory
    cd backend

    # Create and activate a Python virtual environment (e.g., using pyenv)
    python -m venv TopicBook_venv
    source TopicBook_venv/bin/activate
    # Or use pyenv:
     pyenv virtualenv 3.11.13 TopicBook_venv
    pyenv local TopicBook_venv
    
    # Install Python dependencies
    pip install -r requirements.txt 
    ```

3.  **Set up Frontend:**
    ```sh
    # Navigate to the frontend directory
    cd ../frontend
    
    # Install Node.js dependencies
    npm install
    ```

4.  **Configure Environment Variables:**
    The project requires API keys to function.
    * In the `backend` directory, create a `.env` file.
    * ```sh
        touch .env
        ```
    * Open the `.env` file and add your secret keys.
    * **.env template:**
        ```ini
		# 1. Gemini API Key (for the AI model)
		# Get from Google AI Studio: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
		GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

		# 2. Google Cloud API Key (for Search & YouTube)
		# - Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
		# - Create a new project.
		# - Enable "Custom Search API" and "YouTube Data API v3".
		# - Create an API Key in the "Credentials" section.
		GOOGLE_API_KEY="YOUR_GOOGLE_CLOUD_API_KEY_HERE"
		YOUTUBE_API_KEY="PASTE_THE_SAME_GOOGLE_CLOUD_KEY_HERE"

		# 3. Programmable Search Engine ID
		# - Go to [https://programmablesearchengine.google.com/](https://programmablesearchengine.google.com/)
		# - Create a new search engine.
		# - Configure it to "Search the entire web".
		# - Turn ON "Image search".
		# - Copy the "Search engine ID" here.
		SEARCH_ENGINE_ID="YOUR_SEARCH_ENGINE_ID_HERE"
        ```

---
## 🚀 Usage

To run the application, you need to start the Redis service, the backend server, the Celery worker, and the frontend server.

### 1. Ensure Redis is Running
On most systems, Redis runs as a background service after installation. You can check its status with `sudo systemctl status redis`.

### 2. Start the Application Manually
You will need three separate terminals, all navigated to the project root (`TopicBook/`).

* **Terminal 1: Start the FastAPI Server**
    ```sh
    cd backend
    # Activate your virtual environment for venv
    source venv/bin/activate 
	# It automatically activates if it dosent then activate by below command
	pyenv activate TopicBook_venv
    # Run the server
    uvicorn main:app --reload
    ```
* **Terminal 2: Start the Celery Worker**
    ```sh
    cd backend
    # Activate your virtual environment
    source venv/bin/activate
    # Run the worker
    celery -A tasks.celery_app worker --loglevel=info
    ```
* **Terminal 3: Start the React Frontend**
    ```sh
    cd frontend
    # Run the dev server
    npm run dev
    ```

### 3. Start with the Automation Script
Alternatively, you can use the `start.sh` script to run all three application servers with one command from the project root.
```sh
# Make the script executable (only need to do this once)
chmod +x start.sh

# Run the script
./start.sh
```

This will launch all three services. You can now access:

The TopicBook Web App: http://localhost:5173

The Backend API Docs: http://localhost:8000/docs

To stop all services, press Ctrl+C in the terminal where start.sh is running.

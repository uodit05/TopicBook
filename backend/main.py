from fastapi import FastAPI
from pydantic import BaseModel
from tasks import generate_topicbook_task

# Pydantic model to define the structure of our request body
class TopicRequest(BaseModel):
    topic: str
    description: str | None = None

# Create the FastAPI app instance
app = FastAPI()

# A simple root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the TopicBook API!"}

# The endpoint to generate a new TopicBook
@app.post("/generate")
def create_topicbook(request: TopicRequest):
    """
    Accepts a topic and description, and starts the generation task.
    """
    # Start the Celery task in the background
    task = generate_topicbook_task.delay(request.topic, request.description)
    # Return the ID of the task
    return {"task_id": task.id}
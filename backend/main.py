import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from celery.result import AsyncResult
from tasks import generate_topicbook_task, celery_app

# Pydantic model for the request body
class TopicRequest(BaseModel):
    topic: str
    description: str | None = None

app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the TopicBook API!"}

# Endpoint to start the generation task
@app.post("/generate")
def create_topicbook(request: TopicRequest):
    task = generate_topicbook_task.delay(request.topic, request.description)
    return {"task_id": task.id}

# The streaming status endpoint
async def stream_task_status(task_id: str):
    """
    This is an asynchronous generator that yields task status updates.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    last_status = None
    
    while not task_result.ready():
        # Check for new status message in the 'meta' info
        if task_result.info and 'status' in task_result.info:
            current_status = task_result.info['status']
            # If the status has changed, send the update
            if current_status != last_status:
                yield f"data: {current_status}\n\n"
                last_status = current_status
        
        # Wait for a short period before checking again
        await asyncio.sleep(1)

    # Send the final result once the task is complete
    final_result = task_result.result
    yield f"data: {final_result.get('result', 'Task finished with no message.')}\n\n"
    yield f"data: [DONE]\n\n" # Send a special message to signal completion

@app.get("/status/{task_id}")
async def get_task_status(task_id: str, request: Request):
    """
    This endpoint streams the status of a background task to the client.
    """
    return StreamingResponse(stream_task_status(task_id), media_type="text/event-stream")
import asyncio
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from celery.result import AsyncResult
from typing import List
from tasks import generate_topicbook_task, celery_app

class TopicRequest(BaseModel):
    topic: str
    description: str | None = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the TopicBook API!"}

@app.post("/generate")
def create_topicbook(request: TopicRequest):
    task = generate_topicbook_task.delay(request.topic, request.description)
    return {"task_id": task.id}

async def stream_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    last_status = None
    while not task_result.ready():
        if task_result.info and 'status' in task_result.info:
            current_status = task_result.info['status']
            if current_status != last_status:
                yield f"data: {current_status}\n\n"
                last_status = current_status
        await asyncio.sleep(1)
    final_result = task_result.result
    yield f"data: {final_result.get('result', 'Task finished.')}\n\n"
    yield f"data: [DONE]\n\n"

@app.get("/status/{task_id}")
async def get_task_status(task_id: str, request: Request):
    return StreamingResponse(stream_task_status(task_id), media_type="text/event-stream")

BOOKS_DIRECTORY = "Generated-Books"

@app.get("/books", response_model=List[str])
def list_books():
    """
    Lists all the generated .md files in the Generated-Books directory.
    """
    if not os.path.isdir(BOOKS_DIRECTORY):
        return []
    
    try:
        files = sorted([f for f in os.listdir(BOOKS_DIRECTORY) if f.endswith(".md")])
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books/{filename}")
def get_book(filename: str):
    """
    Retrieves the content of a specific book.
    """
    if ".." in filename or filename.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid filename.")
    
    file_path = os.path.join(BOOKS_DIRECTORY, filename)
    
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Book not found.")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"filename": filename, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
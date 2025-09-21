#!/bin/bash

echo "Starting all TopicBook services..."

echo "-> Starting FastAPI server..."
(cd backend && uvicorn main:app --reload) &

echo "-> Starting Celery worker..."
(cd backend && celery -A tasks.celery_app worker --loglevel=info) &

echo "-> Starting Frontend server..."
(cd frontend && npm run dev) &

wait
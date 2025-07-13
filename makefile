# Makefile for Agentic Chatbot
PROJECT_NAME=agentic_chatbot
APP_MODULE=api.chat:app
PYTHONPATH=src
PORT=8000

# Load environment variables from .env if exists
include .env
export

run-dev:
	PYTHONPATH=$(PYTHONPATH) uvicorn $(APP_MODULE) --reload --port $(PORT)

run-prod:
	PYTHONPATH=$(PYTHONPATH) uvicorn $(APP_MODULE) --port $(PORT) --host 0.0.0.0 --workers 2

lint:
	ruff check src api tests

format:
	ruff format src api tests

test:
	PYTHONPATH=$(PYTHONPATH) pytest tests

docker-build:
	docker build -t $(PROJECT_NAME):latest .

docker-run:
	docker run -p $(PORT):$(PORT) --env-file .env $(PROJECT_NAME):latest


# AI Task Manager

A small AI-powered task manager built with **Python, FastAPI, Ollama, and Docker Compose**.

The project explores how to build a local AI agent that can interpret natural-language requests and interact with application functions through tool calling. It runs a local language model, so no paid AI API is required.

## Features

- **Local LLM:** Run Qwen 3.5 4B locally using Ollama.
- **REST API:** Expose endpoints through FastAPI.
- **Task management:** Create and list tasks.
- **AI tool calling:** Let the model request task creation through a Python function.
- **Containerized environment:** Run the application and model using Docker Compose.
- **Interactive API documentation:** Test endpoints through Swagger UI.

## Tech Stack

- Python 3.12
- FastAPI
- Ollama
- Qwen 3.5 4B
- Docker and Docker Compose
- HTTPX

## Prerequisites

Install:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Docker Compose enabled
- Git

On Windows, the project can be run from WSL2 with Ubuntu and Docker Desktop integration enabled.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-task-manager.git
cd ai-task-manager
```

Replace `YOUR-USERNAME` with the GitHub account that hosts this repository.

### 2. Start the application

```bash
make server
```

This builds the FastAPI container, starts the application and Ollama, and downloads the configured model if needed.

The first launch can take several minutes because the model needs to be downloaded. Make sure Docker Desktop is running and has internet access.

### 3. Open the API documentation

Visit:

**http://localhost:8000/docs**

Use the interactive Swagger interface to test the endpoints.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check application health |
| `POST` | `/chat` | Send a message to the local LLM |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List all tasks |
| `POST` | `/agent` | Ask the AI agent to perform a supported action |

### Create a task

`POST /tasks`

Request body:

```json
{
  "title": "Learn Spring Boot"
}
```

Example response:

```json
{
  "id": 1,
  "title": "Learn Spring Boot",
  "completed": false
}
```

### List tasks

`GET /tasks`

Returns the tasks currently stored by the application.

### Use the AI agent

`POST /agent`

Request body:

```json
{
  "message": "Add a task to learn Spring Boot"
}
```

The model can request the `create_task` tool. The FastAPI application executes the function and returns the result.

## Project Structure

```text
ai-task-manager/
├── app/
│   └── main.py
├── compose.yaml
├── Dockerfile
├── Makefile
├── requirements.txt
├── .gitignore
└── README.md
```

## Useful Commands

Start or rebuild the application:

```bash
make server
```

Stop the containers:

```bash
make stop
```

View application and Ollama logs:

```bash
make logs
```

## Current Limitations

This is an educational prototype.

- Tasks are stored in memory and are lost when the application restarts.
- The agent currently supports task creation only.
- The agent does not yet implement a full tool-result feedback loop.
- There is no authentication or multi-user support.

## Roadmap

- [ ] Add task completion and deletion.
- [ ] Let the agent list existing tasks.
- [ ] Implement a complete tool-calling loop.
- [ ] Persist tasks using SQLite.
- [ ] Add automated tests.
- [ ] Improve error handling and validation.
- [ ] Add a web frontend.

## License

No license has been specified yet.

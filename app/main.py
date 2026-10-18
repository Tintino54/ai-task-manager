
import os

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Task Manager")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")


# Temporary in-memory task storage
tasks = []
next_task_id = 1


class ChatRequest(BaseModel):
    message: str


class TaskCreate(BaseModel):
    title: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: ChatRequest):
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": request.message,
                    }
                ],
                "think": False,
                "stream": False,
            },
        )
        response.raise_for_status()
        result = response.json()

    return {"answer": result["message"]["content"]}


@app.post("/tasks", status_code=201)
def create_task(request: TaskCreate):
    global next_task_id

    task = {
        "id": next_task_id,
        "title": request.title,
        "completed": False,
    }

    tasks.append(task)
    next_task_id += 1

    return task


@app.get("/tasks")
def list_tasks():
    return tasks


@app.post("/agent")
async def agent(request: ChatRequest):
    # Describe the function the model is allowed to call.
    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_task",
                "description": "Create a task in the user's task list.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the task.",
                        }
                    },
                    "required": ["title"],
                },
            },
        }
    ]

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": request.message,
                    }
                ],
                "tools": tools,
                "think": False,
                "stream": False,
            },
        )
        response.raise_for_status()
        result = response.json()

    message = result["message"]
    tool_calls = message.get("tool_calls", [])

    # If the model requested a tool, execute it.
    for tool_call in tool_calls:
        function = tool_call["function"]

        if function["name"] == "create_task":
            arguments = function["arguments"]
            created_task = create_task(
                TaskCreate(title=arguments["title"])
            )

            return {
                "answer": f"Created task: {created_task['title']}",
                "task": created_task,
            }

    # Otherwise, return the model's ordinary response.
    return {"answer": message.get("content", "")}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A small CRUD API that manages a to-do list. Data lives in memory only.",
)

# ---------------------------------------------------------------------------
# In-memory "database": just a list of task objects, pre-filled with 3 tasks.
# Restarting the server wipes this — that's the point (databases come in W3).
# ---------------------------------------------------------------------------
tasks = [
    {"id": 1, "title": "Read the assignment", "done": True},
    {"id": 2, "title": "Build the CRUD API", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": False},
]


def next_id() -> int:
    """Return the next free id (max existing id + 1, or 1 if empty)."""
    return max((t["id"] for t in tasks), default=0) + 1


def find_task(task_id: int):
    """Return the task dict with this id, or None."""
    return next((t for t in tasks if t["id"] == task_id), None)


# ---------------------------------------------------------------------------
# Request body schemas
# ---------------------------------------------------------------------------
class TaskCreate(BaseModel):
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# ---------------------------------------------------------------------------
# Stage 1 — root and health endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    """Describe the API — the front door."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    """Liveness check — real companies use exactly this."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Stage 2 — Read: list and single task
# ---------------------------------------------------------------------------
@app.get("/tasks")
def list_tasks():
    """Return the whole list of tasks."""
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Return one task, or 404 if it doesn't exist."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


# ---------------------------------------------------------------------------
# Stage 3 — Create: POST a new task
# ---------------------------------------------------------------------------
@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    """Create a task. Empty/missing title -> 400. Server never trusts the client."""
    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=400, detail="Field 'title' is required and cannot be empty")
    task = {"id": next_id(), "title": payload.title, "done": False}
    tasks.append(task)
    return task


# ---------------------------------------------------------------------------
# Stage 4 — Update & Delete
# ---------------------------------------------------------------------------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    """Replace a task's title and/or done. Unknown id -> 404, empty body -> 400."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if payload.title is None and payload.done is None:
        raise HTTPException(status_code=400, detail="Provide at least 'title' or 'done'")
    if payload.title is not None:
        if not payload.title.strip():
            raise HTTPException(status_code=400, detail="Field 'title' cannot be empty")
        task["title"] = payload.title
    if payload.done is not None:
        task["done"] = payload.done
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Remove a task. Unknown id -> 404. Success returns 204 with empty body."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    tasks.remove(task)
    return None

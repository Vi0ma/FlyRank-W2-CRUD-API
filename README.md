# Task API — FlyRank Internship (Backend Track · Week 2)

A small CRUD API that manages a to-do list: create, read, update, and delete tasks.
Built as part of my **FlyRank internship**, Backend Development Track —
**Week 2, Assignment A1: Build your first CRUD API**.

Built with **FastAPI** (Python). Data lives **only in memory** (a list in the code):
there is no database yet, so restarting the server resets the 3 starting tasks.
That's intentional — persistence arrives in Week 3.

## Install & run

Requires Python 3.10+.

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open **http://localhost:8000/docs** for interactive Swagger UI documentation.

## Endpoints

| Method | Path            | Purpose                     | Success | Errors    |
|--------|-----------------|-----------------------------|---------|-----------|
| GET    | `/`             | Describe the API            | 200     | —         |
| GET    | `/health`       | Check the server is alive   | 200     | —         |
| GET    | `/tasks`        | List all tasks              | 200     | —         |
| GET    | `/tasks/{id}`   | Get one task                | 200     | 404       |
| POST   | `/tasks`        | Create a task               | 201     | 400       |
| PUT    | `/tasks/{id}`   | Update a task               | 200     | 400, 404  |
| DELETE | `/tasks/{id}`   | Delete a task               | 204     | 404       |

A task looks like: `{ "id": 1, "title": "Buy milk", "done": false }`

**Validation**: `POST` and `PUT` reject a missing or empty `title` with a **400**.
Any unknown id returns a **404** with a JSON error, e.g. `{ "detail": "Task 99 not found" }`.

## Example (curl -i)

```
$ curl -si -X POST http://localhost:8000/tasks \
    -H "Content-Type: application/json" -d '{"title":"Buy milk"}'

HTTP/1.1 201 Created
server: uvicorn
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

Open http://localhost:8000/docs and use **Try it out** to run the full CRUD cycle
without curl.

![Swagger UI](swagger.png)

## Context

Project completed as part of my internship at **FlyRank** — Backend Development Track,
Week 2, Assignment A1 ("Build your first CRUD API").

# Task API

A small CRUD API that manages a to-do list — create, read, update, and delete tasks.
Built with **FastAPI** (Python lane) for the FlyRank Backend Track, Week 2.

Data lives **only in memory** (a list in the code). There is no database yet — restarting
the server resets the tasks back to the 3 starting examples. That's intentional (Week 3 fixes it).

## Install & run

Requires Python 3.10+.

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open **http://localhost:8000/docs** for interactive Swagger UI.

## Endpoints

| Method | Path          | Meaning              | Success | Errors        |
|--------|---------------|----------------------|---------|---------------|
| GET    | `/`           | Describe the API     | 200     | —             |
| GET    | `/health`     | Liveness check       | 200     | —             |
| GET    | `/tasks`      | List all tasks       | 200     | —             |
| GET    | `/tasks/{id}` | Get one task         | 200     | 404           |
| POST   | `/tasks`      | Create a task        | 201     | 400           |
| PUT    | `/tasks/{id}` | Update a task        | 200     | 400, 404      |
| DELETE | `/tasks/{id}` | Delete a task        | 204     | 404           |

A task looks like: `{ "id": 1, "title": "Buy milk", "done": false }`

Validation: `POST` and `PUT` reject a missing or empty `title` with **400**.
Any unknown id returns **404** with a JSON error like `{ "detail": "Task 99 not found" }`.

## Example (curl -i)

```
$ curl -si -X POST http://localhost:8000/tasks \
    -H "Content-Type: application/json" -d '{"title":"Buy milk"}'

HTTP/1.1 201 Created
date: Wed, 15 Jul 2026 14:59:24 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

Open http://localhost:8000/docs and use **Try it out** to run the full CRUD cycle
without curl. _(Add your screenshot here — e.g. `![Swagger UI](swagger.png)`.)_

# Task Tracker API

A small REST API for a to-do list, built with Flask and SQLite. You send it HTTP requests to add, list, change and delete tasks, and it stores them in a database file.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"title": "Buy milk"}' http://127.0.0.1:5000/tasks
```

```json
{
  "created_at": "2026-10-12 00:33:09",
  "done": 0,
  "id": 1,
  "title": "Buy milk"
}
```

## What it does

### Endpoints

| Method and URL | What it does | Success code |
|---|---|---|
| `GET /health` | Check the server is running | 200 |
| `GET /tasks` | List all tasks | 200 |
| `POST /tasks` | Add a task. Body: `{"title": "..."}` | 201 |
| `GET /tasks/<id>` | Get one task | 200 |
| `PATCH /tasks/<id>` | Change a task. Body: `{"title": "..."}` and/or `{"done": true}` | 200 |
| `DELETE /tasks/<id>` | Delete a task | 204 |

Every error comes back as JSON, like `{"error": "title is required"}`.

### Input checking

The API checks what it receives and replies with a clear message instead of crashing.

| Problem | Status |
|---|---|
| Body isn't a JSON object | 400 |
| `title` is missing, not text, blank, or longer than 200 characters | 400 |
| `done` is not `true` or `false` | 400 |
| `PATCH` with neither `title` nor `done` | 400 |
| Task id doesn't exist | 404 |
| Unknown URL | 404 |
| Wrong method for a URL (for example `PUT /tasks`) | 405 |

Titles have leading and trailing spaces trimmed before they are saved.

### Files

| File | Purpose |
|---|---|
| `app.py` | The Flask app: URLs, input checking and error replies |
| `db.py` | The SQLite functions: create the table, add, read, update and delete tasks |
| `try_api.sh` | Script that tests every endpoint |
| `requirements.txt` | Python packages needed |
| `LICENSE` | MIT licence |

### How it works

1. `db.py` holds all the SQL, and `app.py` never touches the database directly. That meant I could test the database functions on their own before any web code existed.
2. Every SQL query uses `?` placeholders instead of putting values into the text, which stops SQL injection.
3. `app.py` checks each request before using it, and returns 400 with a reason if something's wrong.

## How to run

```bash
git clone git@github.com:playfu1-d0ubt/task-tracker-api.git
cd task-tracker-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

flask --app app run
```

The API is now at `http://127.0.0.1:5000`. The database file (`tasks.db`) is created automatically the first time it runs.

### Trying it out

With the server running, open a second terminal and run:

```bash
bash try_api.sh
```

This sends 19 requests covering every endpoint, including bad input, and prints the response and status code for each. For predictable task ids, delete `tasks.db` before starting the server.

Some examples:

```bash
# list all tasks
curl http://127.0.0.1:5000/tasks

# mark task 1 as done
curl -X PATCH -H "Content-Type: application/json" -d '{"done": true}' http://127.0.0.1:5000/tasks/1

# delete task 1
curl -X DELETE http://127.0.0.1:5000/tasks/1
```

## Limitations

- There is no login. Anyone who can reach the server can read and change every task.
- It uses Flask's built-in development server, which isn't meant for real traffic.
- There's one shared list, with no users, due dates, filtering or pagination.
- The database file name is fixed in `db.py`.
- The only tests are the `try_api.sh` script. There are no automated `pytest` tests or GitHub Actions workflow yet.

## What I learned

- How HTTP works in practice: methods (`GET`, `POST`, `PATCH`, `DELETE`), status codes and JSON bodies.
- Building an API with Flask and storing data with `sqlite3`.
- Keeping the database code in its own file made it easier to test on its own before adding the web code.
- Using `?` placeholders in SQL, so user input is never part of the query text.
- Validating input and replying with a clear error is a big part of what makes an API usable.

## Ideas for later

- `pytest` tests with Flask's test client, and a GitHub Actions workflow
- A `?done=true` filter and pagination on `GET /tasks`
- Due dates, and a simple API key check
- Running it with `gunicorn` or `waitress`
- A small web page that uses the API as its back end
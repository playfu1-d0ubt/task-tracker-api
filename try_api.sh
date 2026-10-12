#!/usr/bin/env bash
# Exercises every endpoint of the task tracker API.
# Start the server first: flask --app app run
# For predictable ids, delete tasks.db before starting the server.

BASE="http://127.0.0.1:5000"
JSON="Content-Type: application/json"

call() {
  echo
  echo "--- $1"
  shift
  curl -s -w "\nstatus: %{http_code}\n" "$@"
}

# normal use
call "Health check" "$BASE/health"
call "List tasks (empty)" "$BASE/tasks"
call "Create a task" -X POST -H "$JSON" -d '{"title": "Buy milk"}' "$BASE/tasks"
call "Create a task (spaces get trimmed)" -X POST -H "$JSON" -d '{"title": "  Write README  "}' "$BASE/tasks"
call "List tasks" "$BASE/tasks"
call "Get task 1" "$BASE/tasks/1"
call "Mark task 1 done" -X PATCH -H "$JSON" -d '{"done": true}' "$BASE/tasks/1"
call "Rename task 2" -X PATCH -H "$JSON" -d '{"title": "Write the README"}' "$BASE/tasks/2"
call "Delete task 1" -X DELETE "$BASE/tasks/1"
call "Get the deleted task" "$BASE/tasks/1"

# bad input
call "Create: no title" -X POST -H "$JSON" -d '{}' "$BASE/tasks"
call "Create: blank title" -X POST -H "$JSON" -d '{"title": "   "}' "$BASE/tasks"
call "Create: title is a number" -X POST -H "$JSON" -d '{"title": 123}' "$BASE/tasks"
call "Create: not JSON" -X POST -H "$JSON" -d 'not json at all' "$BASE/tasks"
call "Update: done is not true/false" -X PATCH -H "$JSON" -d '{"done": "yes"}' "$BASE/tasks/2"
call "Update: empty body" -X PATCH -H "$JSON" -d '{}' "$BASE/tasks/2"
call "Update: task doesn't exist" -X PATCH -H "$JSON" -d '{"done": true}' "$BASE/tasks/999"
call "Unknown URL" "$BASE/nothing-here"
call "Wrong method" -X PUT "$BASE/tasks"
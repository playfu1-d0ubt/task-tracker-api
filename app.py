"""A small task tracker API built with Flask and SQLite."""

from flask import Flask, jsonify, request
import db

app = Flask(__name__)
db.init_db()  # make sure the table exists when the app starts
MAX_TITLE_LENGTH = 200


def error(message, status):
    """Build a JSON error reply."""
    return jsonify({"error": message}), status


def check_title(title):
    """Return a problem message if the title isn't acceptable, otherwise None."""
    if not isinstance(title, str):
        return "title must be text"
    if not title.strip():
        return "title can't be empty"
    if len(title.strip()) > MAX_TITLE_LENGTH:
        return f"title can't be longer than {MAX_TITLE_LENGTH} characters"
    return None


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(db.get_tasks())


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)  # silent=True gives None instead of crashing
    if not isinstance(data, dict):
        return error("Request body must be a JSON object", 400)
    if "title" not in data:
        return error("title is required", 400)

    problem = check_title(data["title"])
    if problem:
        return error(problem, 400)

    task_id = db.add_task(data["title"].strip())
    return jsonify(db.get_task(task_id)), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_one_task(task_id):
    task = db.get_task(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def change_task(task_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error("Request body must be a JSON object", 400)
    if "title" not in data and "done" not in data:
        return error("Send a title and/or done", 400)

    if "title" in data:
        problem = check_title(data["title"])
        if problem:
            return error(problem, 400)
        data["title"] = data["title"].strip()

    if "done" in data and not isinstance(data["done"], bool):
        return error("done must be true or false", 400)

    task = db.update_task(task_id, title=data.get("title"), done=data.get("done"))
    if task is None:
        return error("Task not found", 404)
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    if not db.delete_task(task_id):
        return jsonify({"error": "Task not found"}), 404
    return "", 204

@app.errorhandler(404)
def page_not_found(e):
    return error("Not found", 404)


@app.errorhandler(405)
def method_not_allowed(e):
    return error("Method not allowed for this URL", 405)
"""A small task tracker API built with Flask and SQLite."""

from flask import Flask, jsonify, request
import db

app = Flask(__name__)
db.init_db()  # make sure the table exists when the app starts

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(db.get_tasks())


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    task_id = db.add_task(data["title"])  # no checking yet, Phase 4 adds it
    return jsonify(db.get_task(task_id)), 201

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_one_task(task_id):
    task = db.get_task(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def change_task(task_id):
    data = request.get_json()
    task = db.update_task(task_id, title=data.get("title"), done=data.get("done"))
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    if not db.delete_task(task_id):
        return jsonify({"error": "Task not found"}), 404
    return "", 204
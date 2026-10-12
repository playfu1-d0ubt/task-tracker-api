"""Database functions for the task tracker (SQLite)."""

import sqlite3

DB_PATH = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us read columns by name
    return conn


def init_db():
    """Create the tasks table if it doesn't exist yet."""
    conn = get_connection()
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    conn.close()

def add_task(title):
    """Add a task and return its new id."""
    conn = get_connection()
    with conn:
        cursor = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.close()
    return cursor.lastrowid


def get_tasks():
    """Return every task as a list of dictionaries."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_task(task_id):
    """Return one task as a dictionary, or None if it doesn't exist."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_task(task_id, title=None, done=None):
    """Change a task's title and/or done flag. Return the updated task, or None."""
    task = get_task(task_id)
    if task is None:
        return None

    new_title = task["title"] if title is None else title
    new_done = task["done"] if done is None else int(done)

    conn = get_connection()
    with conn:
        conn.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (new_title, new_done, task_id),
        )
    conn.close()
    return get_task(task_id)


def delete_task(task_id):
    """Delete a task. Return True if it existed, False if not."""
    conn = get_connection()
    with conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.close()
    return cursor.rowcount > 0
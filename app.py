from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        task TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    data = [{"id": r[0], "name": r[1], "task": r[2]} for r in rows]
    return jsonify(data)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.json
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, task) VALUES (?, ?)", (data["name"], data["task"]))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task added"})

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
    @app.route("/")
def home():
    return "Advanced API is running 🚀"

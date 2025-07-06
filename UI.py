from flask import Flask, request, redirect, render_template, make_response
import sqlite3
import uuid

app = Flask(__name__)

def get_conn():
    return sqlite3.connect("chat.db")

def get_session_id():
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@app.route("/", methods=["GET", "POST"])
def chat():
    session_id = get_session_id()

    if request.method == "POST":
        user_message = request.form["message"]
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, 'user', ?)",
            (session_id, user_message)
        )
        bot_reply = f"Echo: {user_message}"
        cur.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, 'bot', ?)",
            (session_id, bot_reply)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"
    )
    cur.execute(
        "SELECT role, content, timestamp FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
        (session_id,)
    )
    messages = cur.fetchall()
    conn.close()

    resp = make_response(render_template("chat.html", messages=messages))
    resp.set_cookie("session_id", session_id)
    return resp

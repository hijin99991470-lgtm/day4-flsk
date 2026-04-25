import sqlite3
from pathlib import Path

from flask import Flask, abort, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["DATABASE"] = str(Path(__file__).with_name("board.db"))


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()


@app.route("/")
def home():
    return redirect(url_for("post_list"))


@app.route("/posts")
def post_list():
    posts = get_db().execute(
        "SELECT id, title, content, created_at FROM posts ORDER BY id DESC"
    ).fetchall()
    return render_template("posts_list.html", posts=posts)


@app.route("/posts/new", methods=["GET", "POST"])
def post_create():
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()

        if title and content:
            db = get_db()
            db.execute(
                "INSERT INTO posts (title, content) VALUES (?, ?)",
                (title, content),
            )
            db.commit()

        return redirect(url_for("post_list"))

    return render_template("post_form.html")


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = get_db().execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?",
        (post_id,),
    ).fetchone()

    if post is None:
        abort(404)

    return render_template("post_detail.html", post=post)


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)

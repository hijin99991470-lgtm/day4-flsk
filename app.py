import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["DATABASE"] = os.getenv("DATABASE_PATH", str(Path(__file__).with_name("board.db")))


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
    page = request.args.get("page", 1, type=int)
    query = request.args.get("q", "").strip()
    sort = request.args.get("sort", "latest")
    per_page = 5
    db = get_db()

    order_map = {"latest": "id DESC", "oldest": "id ASC", "title": "title ASC"}
    order = order_map.get(sort, "id DESC")

    if query:
        like = f"%{query}%"
        total = db.execute(
            "SELECT COUNT(*) FROM posts WHERE title LIKE ? OR content LIKE ?",
            (like, like),
        ).fetchone()[0]
        posts = db.execute(
            f"SELECT id, title, content, created_at FROM posts WHERE title LIKE ? OR content LIKE ? ORDER BY {order} LIMIT ? OFFSET ?",
            (like, like, per_page, (page - 1) * per_page),
        ).fetchall()
    else:
        total = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        posts = db.execute(
            f"SELECT id, title, content, created_at FROM posts ORDER BY {order} LIMIT ? OFFSET ?",
            (per_page, (page - 1) * per_page),
        ).fetchall()

    total_pages = max(1, (total + per_page - 1) // per_page)
    page = min(max(page, 1), total_pages)

    return render_template(
        "posts_list.html",
        posts=posts,
        page=page,
        total_pages=total_pages,
        query=query,
        sort=sort,
    )


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

    return render_template("write.html", mode="create", post=None)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def post_edit(post_id):
    db = get_db()
    post = db.execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?",
        (post_id,),
    ).fetchone()

    if post is None:
        abort(404)

    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()

        if title and content:
            db.execute(
                "UPDATE posts SET title = ?, content = ? WHERE id = ?",
                (title, content, post_id),
            )
            db.commit()

        return redirect(url_for("post_detail", post_id=post_id))

    return render_template("write.html", mode="edit", post=post)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def post_delete(post_id):
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    return redirect(url_for("post_list"))


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
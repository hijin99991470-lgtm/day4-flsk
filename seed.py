import sys
import io
import os
import sqlite3
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from crawler import fetch_news

DB_PATH = os.getenv("DATABASE_PATH", str(Path(__file__).with_name("board.db")))


def seed():
    news = fetch_news(limit=10)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    added = 0
    for n in news:
        if cur.execute("SELECT 1 FROM posts WHERE title = ?", (n["title"],)).fetchone():
            continue
        cur.execute(
            "INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
            (n["title"], n["summary"], n["pub_date"]),
        )
        added += 1

    conn.commit()
    conn.close()
    print(f"{added}건 추가됨 (전체 {len(news)}건 중)")


if __name__ == "__main__":
    seed()

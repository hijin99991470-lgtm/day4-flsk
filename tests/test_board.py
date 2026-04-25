import tempfile
from pathlib import Path

import pytest

from app import app, init_db


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    app.config.update(TESTING=True, DATABASE=str(db_path))

    with app.app_context():
        init_db()

    with app.test_client() as client:
        yield client


def test_list_page_shows_empty_state(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "게시글 목록" in response.get_data(as_text=True)


def test_create_post_and_show_in_list(client):
    response = client.post(
        "/posts/new",
        data={"title": "첫 글", "content": "내용입니다"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "첫 글" in body


def test_detail_page_shows_post(client):
    client.post(
        "/posts/new",
        data={"title": "상세 제목", "content": "상세 내용"},
        follow_redirects=True,
    )

    response = client.get("/posts/1")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "상세 제목" in body
    assert "상세 내용" in body

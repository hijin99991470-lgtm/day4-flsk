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


def test_create_page_renders_write_form(client):
    response = client.get("/posts/new")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "글쓰기" in body


def test_edit_page_prefills_post(client):
    client.post(
        "/posts/new",
        data={"title": "원본 제목", "content": "원본 내용"},
        follow_redirects=True,
    )

    response = client.get("/posts/1/edit")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "글수정" in body
    assert 'value="원본 제목"' in body
    assert "원본 내용" in body


def test_edit_post_updates_content(client):
    client.post(
        "/posts/new",
        data={"title": "수정 전 제목", "content": "수정 전 내용"},
        follow_redirects=True,
    )

    response = client.post(
        "/posts/1/edit",
        data={"title": "수정 후 제목", "content": "수정 후 내용"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "수정 후 제목" in body
    assert "수정 후 내용" in body


def test_detail_page_shows_edit_delete_buttons_and_confirm(client):
    client.post(
        "/posts/new",
        data={"title": "버튼 확인", "content": "내용"},
        follow_redirects=True,
    )

    response = client.get("/posts/1")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "/posts/1/edit" in body
    assert "/posts/1/delete" in body
    assert "정말 삭제할까요?" in body


def test_delete_post_removes_item(client):
    client.post(
        "/posts/new",
        data={"title": "삭제 대상", "content": "삭제 내용"},
        follow_redirects=True,
    )

    response = client.post("/posts/1/delete", follow_redirects=True)

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "삭제 대상" not in body

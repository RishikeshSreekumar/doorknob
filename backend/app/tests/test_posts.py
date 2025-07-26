from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


def test_create_post(client: TestClient, test_user: User):
    response = client.post(
        "/posts/",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        json={"title": "Test Post", "content": "This is a test post."},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"
    assert response.json()["content"] == "This is a test post."
    assert response.json()["owner_id"] == test_user["id"]


def test_get_post(client: TestClient, test_post: dict):
    response = client.get(f"/posts/{test_post['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == test_post["title"]
    assert response.json()["content"] == test_post["content"]


def test_update_post(client: TestClient, test_user: User, test_post: dict):
    response = client.put(
        f"/posts/{test_post['id']}",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        json={"title": "Updated Post", "content": "This is an updated post."},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Post"
    assert response.json()["content"] == "This is an updated post."


def test_delete_post(client: TestClient, test_user: User, test_post: dict):
    response = client.delete(
        f"/posts/{test_post['id']}",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_post["id"]

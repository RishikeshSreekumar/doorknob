import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


class TestAuth:
    @pytest.fixture
    def client(self):
        from backend.main import app
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db
        yield TestClient(app)
        app.dependency_overrides = {}
        Base.metadata.drop_all(bind=engine)

    def test_register(self, client):
        response = client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_register_duplicate_email(self, client):
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        response = client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_login(self, client):
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "testpassword"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_incorrect_password(self, client):
        client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

import pytest
from fastapi.testclient import TestClient

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from anirecs.backend.app.models import Base
from anirecs.backend.app.database import get_db
from anirecs.backend.app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite://"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


# New database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Test client setup
@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


# Test to ensure that a new user can sign up successfully
def test_sign_user_up_success(test_client):
    form_data = {
        "username": "newuser",
        "password": "securepassword"
    }

    response = test_client.post("/sign_up/", data=form_data)

    assert response.status_code == 200
    response_data = response.json()

    assert "id" in response_data
    assert response_data["username"] == "newuser"


def test_read_users_me(test_client):
    # Sign in to get a valid token
    form_data = {
        "username": "newuser",
        "password": "securepassword"
    }

    response = test_client.post("/token", data=form_data)

    assert response.status_code == 200
    token = response.json()["access_token"]

    # Use the token to request user information
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = test_client.get("/users/me/", headers=headers)

    assert response.status_code == 200
    response_data = response.json()

    assert response_data["username"] == "newuser"


def test_read_users_me_invalid_token(test_client):
    # Attempt to access user information with an invalid token
    headers = {
        "Authorization": "Bearer invalid_token"
    }

    response = test_client.get("/users/me/", headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

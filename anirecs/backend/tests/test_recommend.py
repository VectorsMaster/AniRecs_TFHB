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


# Helper function to get a valid token
def get_token(test_client, username, password):
    # Sign in to get a valid token
    form_data = {
        "username": username,
        "password": password,
    }
    response = test_client.post("/token", data=form_data)
    return response.json()["access_token"]


def test_recommend_basic(test_client):
    # Create test user and get a token
    form_data = {
        "username": "userrecommended",
        "password": "userrecommendedpass",
    }
    test_client.post("/sign_up/", data=form_data)

    token = get_token(test_client, "userrecommended", "userrecommendedpass")

    # Create some anime and tags
    response = test_client.post("/anime/", json={
        "title": "Anime 1",
        "description": "Description for Anime 1",
        "rank": 8,
        "main_picture": "http://example.com/image.jpg",
        "tags": ["Action", "Adventure"],
    })

    test_client.post("/anime/", json={
        "title": "Recommended Anime",
        "description": "Description for Recommended Anime",
        "rank": 7,
        "main_picture": "http://example.com/image.jpg",
        "tags": ["Fantasy", "Action"],
    })

    anime_id = response.json()["id"]

    # Add Anime 1 to user history (already watched)
    headers = {
        "Authorization": f"Bearer {token}",
    }

    test_client.post(f"/watch/{anime_id}", headers=headers)

    # Retrieve recommendations
    response = test_client.get("/recommend", headers=headers)

    assert response.status_code == 200

    titles = [anime["title"] for anime in response.json()["animes"]]

    # Check if "Recommended Anime" is in the list of titles
    assert "Recommended Anime" in titles

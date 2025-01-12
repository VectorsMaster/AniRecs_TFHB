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
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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


# Test watching a new anime
def test_watch_anime_success(test_client):
    # Create test user
    form_data = {
        "username": "viewer",
        "password": "viewerpass",
    }
    test_client.post("/sign_up/", data=form_data)

    # Get token
    token = get_token(test_client, "viewer", "viewerpass")

    # Create a test anime
    anime_data = {
        "title": "Random Anime",
        "description": "Description of Random Anime",
        "rank": 8,
        "main_picture": "http://example.com/image.jpg",
        "tags": ["Action"],
    }
    response = test_client.post("/anime/", json=anime_data)

    assert response.status_code == 200
    anime_id = response.json()["id"]  # Store the created anime's ID

    # Use the token to watch the anime
    headers = {
        "Authorization": f"Bearer {token}",
    }

    anime_response = test_client.get(f"/animes/{anime_id}")
    assert anime_response.status_code == 200

    response = test_client.post(
        f"/watch/{anime_response.json()['id']}", headers=headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Random Anime"


# Test watching the same anime twice
def test_watch_anime_duplicate(test_client):
    # Create test user
    form_data = {
        "username": "viewer",
        "password": "viewerpass",
    }
    test_client.post("/sign_up/", data=form_data)

    # Get token
    token = get_token(test_client, "viewer", "viewerpass")

    # Create a test anime
    anime_data = {
        "title": "Fun Anime",
        "description": "Description of Fun Anime",
        "rank": 5,
        "main_picture": "http://example.com/image.jpg",
        "tags": ["Comedy"],
    }
    response = test_client.post("/anime/", json=anime_data)
    anime_id = response.json()["id"]

    # Use the token to watch the anime
    headers = {
        "Authorization": f"Bearer {token}",
    }

    anime_response = test_client.get(f"/animes/{anime_id}")

    response = test_client.post(
        f"/watch/{anime_response.json()['id']}", headers=headers
    )

    # Watch the same anime
    response = test_client.post(
        f"/watch/{anime_response.json()['id']}", headers=headers
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "This anime is already watched by current user"
    }


# Test getting the user's watch history
def test_get_my_history(test_client):
    # Get token
    token = get_token(test_client, "viewer", "viewerpass")

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = test_client.get("/history", headers=headers)
    assert response.status_code == 200

    # Extract all titles from the response
    titles = [anime["title"] for anime in response.json()["animes"]]

    # Check if the animes are in the list of titles
    assert "Random Anime" in titles
    assert "Fun Anime" in titles

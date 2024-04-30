import pytest
from fastapi.testclient import TestClient

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

import random
import string

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


# Helper function to create random strings
def random_string(length=10):
    return ''.join(
        random.choice(string.ascii_lowercase) for _ in range(length)
    )


# Test search by title
def test_search_by_title(test_client):
    # Create some anime
    anime_data = [
        {"title": "Naruto",
         "description": "Ninja adventures",
         "rating": 9.5,
         "tags": ["Action"]},
        {"title": "Bleach",
         "description": "Soul Reapers",
         "rating": 8.5,
         "tags": ["Action", "Fantasy"]},
        {"title": "One Piece",
         "description": "Pirate adventures",
         "rating": 7.5,
         "tags": ["Adventure"]},
    ]

    for anime in anime_data:
        test_client.post("/anime/", json=anime)

    # Search for anime by title
    response = test_client.get("/animes?title=Naruto")

    assert response.status_code == 200

    # Extract all titles from the response
    titles = [anime["title"] for anime in response.json()["animes"]]

    # Check if the animes are in the list of title
    assert "Naruto" in titles


# Test search by title lower and upper case
def test_search_by_title_lower(test_client):
    response = test_client.get("/animes?title=nArUto")

    assert response.status_code == 200

    # Extract all titles from the response
    titles = [anime["title"] for anime in response.json()["animes"]]

    # Check if the animes are in the list of title
    assert "Naruto" in titles


# Test search by description
def test_search_by_description(test_client):
    response = test_client.get("/animes?description=pirate")

    assert response.status_code == 200

    # Extract all titles from the response
    titles = [anime["title"] for anime in response.json()["animes"]]

    # Check if the animes are in the list of title
    assert "One Piece" in titles


# Test search by genre
def test_search_by_genre(test_client):
    response = test_client.get("/animes?genre=fantasy")

    assert response.status_code == 200

    # Extract all titles from the response
    titles = [anime["title"] for anime in response.json()["animes"]]

    # Check if the animes are in the list of title
    assert "Bleach" in titles


# Test search with no results
def test_search_no_results(test_client):
    response = test_client.get("/animes?title=nonexistentanime")

    assert response.status_code == 200
    results = response.json()["animes"]

    assert len(results) == 0


# Test random search
def test_random_search(test_client):
    # Create anime with random titles and descriptions
    random_titles = [random_string() for _ in range(5)]

    for title in random_titles:
        test_client.post("/anime/", json={
            "title": title,
            "description": f"Description of {title}",
            "rating": random.uniform(5.0, 10.0),
            "tags": [random.choice(["Action", "Comedy", "Sci-Fi"])],
        })

    # Random search
    search_term = random.choice(random_titles)
    response = test_client.get(f"/animes?title={search_term}")

    assert response.status_code == 200
    # Extract all titles from the response
    titles = [anime["title"] for anime in response.json()["animes"]]

    # Check if the animes are in the list of title
    assert search_term in titles

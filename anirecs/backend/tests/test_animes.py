import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from anirecs.backend.app.database import get_db, Base
from anirecs.backend.app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite://"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./anirecs/backend/test/test_app.db"

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


# Test case to check if a new anime can be created
def test_create_anime(test_client):
    # Given
    new_anime = {
        "title": "Anime test",
        "description": "Description test",
        "rating": 9,
        "tags": ["Comedy", "Action"]
    }

    # When
    response = test_client.post("/anime/", json=new_anime)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == new_anime["title"]
    assert data["description"] == new_anime["description"]
    assert data["rating"] == new_anime["rating"]
    assert "Action" in [tag["name"] for tag in data["tags"]]
    assert "Comedy" in [tag["name"] for tag in data["tags"]]


# Test case for handling anime not found
def test_read_anime_not_found(test_client):
    # When
    response = test_client.get("/animes/100")

    # Then
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


# Test reading an anime by ID
def test_read_anime_get(test_client):
    anime_data = {
        "title": "Drama Test Anime",
        "description": "Drama Anime Description",
        "rating": 8,
        "tags": ["Drama", "Fantasy"],
    }
    create_response = test_client.post("/anime/", json=anime_data)
    anime_id = create_response.json()["id"]  # Get the anime ID

    response = test_client.get(f"/animes/{anime_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Drama Test Anime"
    assert data["description"] == "Drama Anime Description"
    assert data["rating"] == 8
    assert "Drama" in [tag["name"] for tag in data["tags"]]
    assert "Fantasy" in [tag["name"] for tag in data["tags"]]

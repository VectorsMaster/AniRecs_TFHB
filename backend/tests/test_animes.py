import pytest
from unittest.mock import MagicMock
from backend.app.schemas.animes import AnimeCreate
from backend.app.CRUD import AnimeService


def test_add_existed_anime():
    session_instance = MagicMock()
    anime = AnimeCreate(
        title="Test title",
        description="Test description",
        rank=1,
        tags=["action"],
        main_picture="https://main.picture",
    )
    session_instance.add.side_effect = Exception("This anime exists")
    with pytest.raises(Exception, match="This anime exists"):
        AnimeService.add_anime(anime, db=session_instance)


def test_retrieve_anime():

    session_instance = MagicMock()
    session_instance.query.return_value.filter.return_value.first.return_value = {
        "title": "Test title",
        "description": "Test description",
        "rank": 1,
        "tags": ["action"],
        "main_picture": "https://main.picture",
    }

    res = AnimeService.retrieve_anime(1, db=session_instance)
    assert res["title"] == "Test title"

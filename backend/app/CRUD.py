from fastapi import Depends
from sqlalchemy.orm import Session


from backend.app.schemas.animes import AnimeCreate
from backend.app.models import Anime, Tag
from backend.app.database import get_db


class AnimeService:

    @staticmethod
    def add_anime(anime: AnimeCreate, db: Session):
        new_anime = Anime(
            title=anime.title,
            description=anime.description,
            rank=anime.rank,
            main_picture=anime.main_picture,
        )

        # Handle tags
        for tag_name in anime.tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)  # Create new tag if it doesn't exist
            new_anime.tags.append(tag)  # Associate tag with anime

        db.add(new_anime)
        db.commit()
        db.refresh(new_anime)

        return new_anime

    @staticmethod
    def retrieve_anime(anime_id: int, db: Session):
        db_item = db.query(Anime).filter(Anime.id == anime_id).first()
        return db_item

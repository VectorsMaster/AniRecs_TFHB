from fastapi import Depends
from sqlalchemy.orm import Session


from anirecs.backend.app.schemas.animes import AnimeCreate
from anirecs.backend.app.models import Anime, Tag
from anirecs.backend.app.database import get_db


class AnimeService:

    @classmethod
    def add_anime(cls, anime: AnimeCreate, db: Session = Depends(get_db)):
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

    @classmethod
    def retrieve_anime(cls, anime_id: int, db: Session = Depends(get_db)):
        db_item = db.query(Anime).filter(Anime.id == anime_id).first()
        return db_item

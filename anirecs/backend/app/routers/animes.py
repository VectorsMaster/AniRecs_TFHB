from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from anirecs.backend.app.models import Anime, Tag
from anirecs.backend.app.schemas.animes import (
    AnimeCreate,
    AnimeResponse,
    AnimesResponse,
    convert
)
from anirecs.backend.app.database import get_db

router = APIRouter()


# API endpoint to create an anime
# @router.post("/animes/", response_model=AnimeResponse)
# async def create_item(item: AnimeCreate, db: Session = Depends(get_db)):
#     db_item = Anime(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


# API endpoint to create an anime
@router.post("/anime/", response_model=AnimeResponse)
def create_anime(anime: AnimeCreate, db: Session = Depends(get_db)):
    # Create new anime
    new_anime = Anime(
            title=anime.title,
            description=anime.description,
            rating=anime.rating
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


# API endpoint to create an item
@router.get("/animes/{anime_id}", response_model=AnimeResponse)
def read_item(anime_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Anime).filter(Anime.id == anime_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item


@router.get("/animes", response_model=AnimesResponse)
async def search(
    title: str | None = None,
    description: str | None = None,
    genre: str | None = None,
    db: Session = Depends(get_db)
):
    if title:
        title = title.lower()
        return convert(
            db.query(Anime).filter(
                func.lower(Anime.title).like(f"%{title}%")
            ).all()[0:10]
        )
    if description:
        description = description.lower()
        return convert(
            db.query(Anime).filter(
                func.lower(Anime.description).like(f"%{description}%")
            ).all()[0:10]
        )
    if genre:
        genre = genre.lower()
        return convert(
            db.query(Anime).filter(
                Anime.tags.any(func.lower(Tag.name) == genre)
            ).all()[0:10]
        )
    return AnimesResponse()

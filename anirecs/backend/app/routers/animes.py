from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Anime, Tag
from schemas.animes import AnimeCreate, AnimeResponse
from database import get_db

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

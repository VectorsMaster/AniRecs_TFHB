from typing import Annotated
import requests

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from anirecs.backend.app.routers.users import get_current_user
from anirecs.backend.app.models import Anime, Tag
from anirecs.backend.app.schemas.users import UserResponse
from anirecs.backend.app.schemas.animes import (
    AnimeCreate,
    AnimeResponse,
    AnimesResponse,
    convert,
)
from anirecs.backend.app.CRUD import AnimeService
from anirecs.backend.app.database import get_db
from anirecs.backend.settings import CLIENT_ID

router = APIRouter()


# API endpoint to populate the database using external source
# Can be accessed only by the root user
@router.post("/populate")
async def populate(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    pages: int = 1,
    db: Session = Depends(get_db),
):
    if current_user.username != "root":
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only root user can populate the database",
        )

    url = "https://api.myanimelist.net/v2/anime/"
    url = url + "ranking?ranking_type=all&limit=100"
    headers = {"X-MAL-CLIENT-ID": CLIENT_ID}
    print(url)
    result = 0
    for i in range(pages):
        response = requests.get(
            url + f"&fields=id,title,rank,genres,synopsis&offset={result}",
            headers=headers,
            timeout=2,
        )
        if response.status_code != 200:
            break

        result += 100
        if len(response.json()["data"]) != 100:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Unexpected number of received animes",
            )

        for item in response.json()["data"]:
            anime = Anime(
                title=item["node"]["title"],
                description=item["node"]["synopsis"],
                rank=int(item["node"]["rank"]),
                main_picture=item["node"]["main_picture"]["large"],
            )

            if not item["node"].get("genres"):
                db.add(anime)
                db.commit()
                continue

            for genre in item["node"]["genres"]:
                tag = db.query(Tag).filter(Tag.name == genre["name"]).first()
                if tag is None:
                    tag = Tag(name=genre["name"])

                anime.tags.append(tag)

            db.add(anime)
            db.commit()

    return {"anime_count": result}


# API endpoint to create an anime
@router.post("/anime/", response_model=AnimeResponse)
def create_anime(anime: AnimeCreate):
    return AnimeService.add_anime(anime)


# API endpoint to create an item
@router.get("/animes/{anime_id}", response_model=AnimeResponse)
def read_item(anime_id: int):
    db_item = AnimeService.retrieve_anime(anime_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item


@router.get("/animes", response_model=AnimesResponse)
async def search(
    title: str | None = None,
    description: str | None = None,
    genre: str | None = None,
    db: Session = Depends(get_db),
):
    if title:
        title = title.lower()
        return convert(
            db.query(Anime)
            .filter(func.lower(Anime.title).like(f"%{title}%"))
            .all()[0:10]
        )
    if description:
        description = description.lower()
        return convert(
            db.query(Anime)
            .filter(func.lower(Anime.description).like(f"%{description}%"))
            .all()[0:10]
        )
    if genre:
        genre = genre.lower()
        return convert(
            db.query(Anime)
            .filter(Anime.tags.any(func.lower(Tag.name) == genre))
            .all()[0:10]
        )
    return convert(db.query(Anime).all())

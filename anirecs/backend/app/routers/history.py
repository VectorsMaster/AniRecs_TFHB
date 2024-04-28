from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from anirecs.backend.app.schemas.users import UserResponse
from anirecs.backend.app.routers.users import get_current_user
from sqlalchemy.orm import Session
from anirecs.backend.app.schemas.animes import AnimeResponse, TagResponse
from anirecs.backend.app.database import get_db
from anirecs.backend.app.models import Anime, AnimeHistory, User
from anirecs.backend.app.schemas.history import HistoryResponse
router = APIRouter()


@router.post("/watch/{anime_id}", response_model=AnimeResponse)
def watch(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    anime_id: int,
    db: Session = Depends(get_db)
):
    anime = db.query(Anime).filter(Anime.id == anime_id).first()

    if not anime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This is not a valid anime"
        )

    watched = db.query(AnimeHistory).filter(
            AnimeHistory.anime_id == anime.id,
            AnimeHistory.user_id == current_user.id
        ).first()

    if watched:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This anime is already watched by current user"
        )

    watched = AnimeHistory(user_id=current_user.id, anime_id=anime_id)
    db.add(watched)
    db.commit()
    return anime


@router.get("/history", response_model=HistoryResponse)
def get_my_history(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    user_history = HistoryResponse()
    for anime in user.history:
        current_anime = db.query(Anime).filter(
                Anime.id == anime.anime_id
            ).first()
        anime_res = AnimeResponse.model_validate(current_anime.__dict__)
        print(current_anime.tags)
        for tag in current_anime.tags:
            anime_res.tags.append(TagResponse.model_validate(tag.__dict__))

        user_history.animes.append(anime_res)
    return user_history

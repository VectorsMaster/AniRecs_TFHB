from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.schemas.users import UserResponse
from backend.app.schemas.animes import AnimesResponse, convert
from backend.app.routers.users import get_current_user
from backend.app.models import User, Anime
from backend.app.database import get_db


router = APIRouter()


@router.get("/recommend", response_model=AnimesResponse)
def recommend(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    tag_occurences = {}
    watched = {}
    for history_item in user.history:
        anime = history_item.anime
        watched[anime.title] = 1
        for tag in anime.tags:
            val = tag_occurences.get(tag.name)
            if val:
                tag_occurences[tag.name] = val + 1
            else:
                tag_occurences[tag.name] = 1

    all_animes = db.query(Anime).all()
    recommendation_list = []
    for anime in all_animes:
        is_watched = watched.get(anime.title)
        if is_watched:
            continue
        score = 0
        for tag in anime.tags:
            scale = tag_occurences.get(tag.name)
            if scale:
                score += scale
        recommendation_list.append(((-score, anime.rank), anime))

    recommendation_list.sort(key=lambda x: x[0])
    return convert([item[1] for item in recommendation_list[0:10]])

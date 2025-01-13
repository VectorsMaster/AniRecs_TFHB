from typing import List
from pydantic import BaseModel


class TagResponse(BaseModel):
    name: str


# Pydantic model for request data
class AnimeCreate(BaseModel):
    title: str
    description: str
    rank: int
    main_picture: str = ""
    tags: List[str] = []


# Pydantic model for response data
class AnimeResponse(BaseModel):
    id: int
    title: str
    description: str
    rank: int
    main_picture: str
    tags: List[TagResponse] = []


class AnimesResponse(BaseModel):
    animes: List[AnimeResponse] = []


def convert(animes) -> AnimesResponse:
    response = AnimesResponse()
    for anime in animes:
        anime_res = AnimeResponse(
            id=anime.id,
            title=anime.title,
            description=anime.description,
            rank=anime.rank,
            main_picture=anime.main_picture,
            tags=[],
        )
        for tag in anime.tags:
            anime_res.tags.append(TagResponse(name=tag.name))
        response.animes.append(anime_res)
    return response

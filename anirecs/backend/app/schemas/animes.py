from typing import List
from pydantic import BaseModel


class TagResponse(BaseModel):
    name: str


# Pydantic model for request data
class AnimeCreate(BaseModel):
    title: str
    description: str
    rating: float
    tags: List[str] = []

    class Config:
        orm_mode = True
        from_attributes = True
        # allow_population_by_field_name = True


# Pydantic model for response data
class AnimeResponse(BaseModel):
    id: int
    title: str
    description: str
    rating: float
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
            rating=anime.rating,
            tags=[]
        )
        for tag in anime.tags:
            anime_res.tags.append(TagResponse(name=tag.name))
        response.animes.append(anime_res)
    return response

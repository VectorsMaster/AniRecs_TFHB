from typing import List
from pydantic import BaseModel


# Pydantic model for request data
class AnimeCreate(BaseModel):
    title: str
    description: str
    rating: float
    # tags: List[str]


# Pydantic model for response data
class AnimeResponse(BaseModel):
    id: int
    title: str
    description: str
    rating: float
    # tags: List[str]

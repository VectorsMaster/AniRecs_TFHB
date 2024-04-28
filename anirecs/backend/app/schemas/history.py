from typing import List

from pydantic import BaseModel
from schemas.animes import AnimeResponse


class HistoryResponse(BaseModel):
    animes: List[AnimeResponse] = []

from typing import List

from pydantic import BaseModel
from anirecs.backend.app.schemas.animes import AnimeResponse


class HistoryResponse(BaseModel):
    animes: List[AnimeResponse] = []

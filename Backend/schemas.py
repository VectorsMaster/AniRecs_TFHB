from pydantic import BaseModel


# Pydantic model for request data
class ItemCreate(BaseModel):
    name: str
    description: str


# Pydantic model for response data
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
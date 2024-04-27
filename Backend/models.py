from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ARRAY, Double
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Anime(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    rating = Column(Double)
    # tags = Column(ARRAY(String))

class AnimeHistory(Base):
    __tablename__ = "anime_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    anime_id = Column(Integer, ForeignKey('animes.id'))

    user = relationship("User", back_populates="history")
    anime = relationship("Anime", back_populates="watched_by")

User.history = relationship("AnimeHistory", back_populates="user")
Anime.watched_by = relationship("AnimeHistory", back_populates="anime")
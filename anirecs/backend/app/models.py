from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from anirecs.backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Anime(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    main_picture = Column(String)
    rank = Column(Integer)
    tags = relationship(
        "Tag",
        secondary="anime_tag",
        back_populates="animes"
    )


class AnimeHistory(Base):
    __tablename__ = "anime_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    anime_id = Column(Integer, ForeignKey('animes.id'))

    user = relationship("User", back_populates="history")
    anime = relationship("Anime", back_populates="watched_by")


anime_tag = Table(
    "anime_tag",
    Base.metadata,
    Column("anime_id", ForeignKey("animes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    animes = relationship(
            "Anime",
            secondary="anime_tag",
            back_populates="tags"
        )


User.history = relationship("AnimeHistory", back_populates="user")
Anime.watched_by = relationship("AnimeHistory", back_populates="anime")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from anirecs.backend.settings import database_settings
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{database_settings.DataBase_User}"
    f":{database_settings.DataBase_Password}@"
    f"{database_settings.DataBase_URL}/"
    f"{database_settings.DataBase_Name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get the database session
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

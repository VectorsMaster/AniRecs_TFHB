from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from anirecs.backend.app.secrets import root_p
from anirecs.backend.app.models import User
from anirecs.backend.app.database import engine, Base, SessionLocal
from anirecs.backend.app.routers import (
    animes,
    users,
    history,
    recommend
)

# Create tables
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def moderator():
    db = SessionLocal()
    user = db.query(User).filter(User.username == 'root').first()
    if not user:
        user = User(
            username='root',
            hashed_password=pwd_context.hash(root_p)
        )
        db.add(user)
        db.commit()

    db.close()


def release():
    return


@asynccontextmanager
async def lifespan(app: FastAPI):
    moderator()
    yield release()

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(animes.router)
app.include_router(users.router)
app.include_router(history.router)
app.include_router(recommend.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    moderator()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

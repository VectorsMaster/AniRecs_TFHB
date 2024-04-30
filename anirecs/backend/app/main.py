from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from anirecs.backend.app.database import engine, Base
from anirecs.backend.app.routers import animes, users, history, recommend

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

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
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

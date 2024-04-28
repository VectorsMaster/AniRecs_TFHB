from fastapi import FastAPI

from anirecs.backend.app.database import engine, Base
from anirecs.backend.app.routers import animes, users, history

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(animes.router)
app.include_router(users.router)
app.include_router(history.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

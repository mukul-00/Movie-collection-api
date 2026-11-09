from fastapi import FastAPI

from app.routes.movie_routes import router as movie_router
from app.routes.user_routes import router as user_router

from app.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(movie_router)
app.include_router(user_router)

@app.get('/')
def home():
    return {"message": "Movie Collection API is running!"}


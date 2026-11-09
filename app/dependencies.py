from app.database import SessionLocal

from fastapi.security import OAuth2PasswordBearer

from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import select

from jose import jwt, JWTError

from app.config import settings
from app.crud import user_crud
from app.models import User, Movie

from app.crud import movie_crud


def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = user_crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return user


        

def get_current_user_movie(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_movie = movie_crud.get_movie(db, id)

    if existing_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if existing_movie.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to access this movie.")
    
    return existing_movie

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
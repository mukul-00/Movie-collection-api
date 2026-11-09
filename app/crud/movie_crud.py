from typing import Optional

import math 

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.schemas import MovieCreate, MovieUpdate
from app.models import Movie, User
from app.helper import apply_filters, apply_sort, apply_pagination


def create_movie(db: Session, movie: MovieCreate, user_id: int):
    movie_db = Movie(
        title=movie.title,
        director=movie.director,
        genre=movie.genre,
        rating=movie.rating,
        release_year=movie.release_year,
        user_id = user_id
    )
    db.add(movie_db)
    db.commit()
    db.refresh(movie_db)

    return movie_db



def get_movie(db: Session, id: int):

    statement = select(Movie).where(Movie.id == id)
    result = db.execute(statement).scalar_one_or_none()

    return result


def delete_movie(db: Session, id: int):

    statement = select(Movie).where(Movie.id == id)
    movie = db.execute(statement).scalar_one_or_none()

    if movie is None:
        return None
    
    db.delete(movie)
    db.commit()

    return movie


def update_movie(db: Session, id: int, movie: MovieUpdate):

    statement = select(Movie).where(Movie.id == id)
    movie_db = db.execute(statement).scalar_one_or_none()

    if movie_db is None:
        return None
    
    movie_db.title = movie.title
    movie_db.director = movie.director
    movie_db.genre = movie.genre
    movie_db.rating = movie.rating
    movie_db.release_year = movie.release_year

    db.commit()
    db.refresh(movie_db)

    return movie_db


# Optiional[] = None is same as <=> | None = None
def get_movies(
        db: Session, 
        search: Optional[str] = None,
        genre: Optional[str] = None, 
        rating: Optional[float] = None,
        sort: Optional[str] = None,
        page: int = 1,
        limit: int = 10
    ):
    
    statement = select(Movie)
    statement = apply_filters(statement, search, genre, rating)
    statement = apply_sort(statement, sort)
    statement = apply_pagination(statement, page, limit)
    movies = db.execute(statement).scalars().all()

    count_statement = select(func.count()).select_from(Movie)
    count_statement = apply_filters(count_statement, search, genre, rating)
    total = db.execute(count_statement).scalar_one()

    pages = math.ceil(total/limit)

    return {"total": total, "page": page, "limit": limit, "pages": pages, "items": movies}


# def get_movies_by_user(db: Session, user_id: int):

#     statement = select(Movie).where(Movie.user_id == user_id) 
#     movies = db.execute(statement).scalars().all()

#     return movies


def get_my_movies(db: Session, user_id: int, page: int, limit: int):

    statement = select(Movie).where(Movie.user_id == user_id)
    statement = apply_pagination(statement, page, limit)
    movies = db.execute(statement).scalars().all()

    count_statement = select(func.count()).select_from(Movie).where(Movie.user_id == user_id)
    total = db.execute(count_statement).scalar_one()

    pages = math.ceil(total/limit)

    return {"total": total, "page": page, "limit": limit, "pages": pages, "items": movies}


def get_movies_by_user(db: Session, user_id: int):

    user = db.get(User, user_id)
    if user is None:
        return None
    statement = select(Movie).where(Movie.user_id == user_id)
    movies = db.execute(statement).scalars().all()
    return movies


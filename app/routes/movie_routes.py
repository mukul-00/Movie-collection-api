from fastapi import APIRouter, Depends, HTTPException, Query


from sqlalchemy.orm import Session

from app.schemas import MovieCreate, MovieResponse, MovieUpdate, MovieListResponse
from app.crud import movie_crud
from app.dependencies import get_db
from app.models import User, Movie
from app.dependencies import get_current_user, get_current_user_movie

from typing import Optional



router = APIRouter()

@router.post('/movies', response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return movie_crud.create_movie(db, movie, current_user.id)


# @router.get("/movies", response_model=list[MovieResponse])
# def get_all_movies(db: Session = Depends(get_db)):
#     return crud.get_movies(db)


@router.get("/movies/{id}", response_model=MovieResponse)
def get_movie(id: int, db: Session = Depends(get_db)):
    
    result = movie_crud.get_movie(db, id)

    if result is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return result


@router.delete("/movies/{id}", status_code=204)
def delete_movie(db: Session = Depends(get_db), movie_db: Movie = Depends(get_current_user_movie)):
    
    movie_crud.delete_movie(db, movie_db.id)
    return 


@router.put("/movies/{id}", response_model=MovieResponse)
def update_movie(movie: MovieUpdate, id: int, db: Session = Depends(get_db), movie_db: Movie = Depends(get_current_user_movie)):
    
    return movie_crud.update_movie(db, movie_db.id, movie)

    


# @router.get("/movies", response_model=list[MovieResponse])
# def search_movies(search : Optional[str] = None, db: Session = Depends(get_db)):
    
#     if search is None:
#         # get all the movies
#         return crud.get_movies(db)
    
#     # get movie by search 
#     return crud.search_movies(db, search)

@router.get('/movies', response_model=MovieListResponse)
def get_movies(db: Session = Depends(get_db), 
               search: Optional[str] = None, 
               genre: Optional[str] = None, 
               rating: Optional[float] = None, 
               sort: Optional[str] = None, 
               page: int = Query(1, ge=1), 
               limit: int = Query(10, ge=1, le=100)
               ):

    result = movie_crud.get_movies(db, search, genre, rating, sort, page, limit)

    if result["total"] > 0 and page > result["pages"]:
        raise HTTPException(status_code=404, detail="Page not found")

    return result
        

@router.get("/me/movies", response_model=MovieListResponse)
def get_me_movies(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), current_user: User = Depends(get_current_user),):

    result = movie_crud.get_my_movies(db, current_user.id, page, limit)

    if result["total"] > 0 and page > result["pages"]:
        raise HTTPException(status_code=404, detail="Page not found")

    return result


@router.get("/users/{id}/movies", response_model=list[MovieResponse])
def get_movies_by_user(id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if current_user.id != id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You are not allowed to access this user's movies.")

    result = movie_crud.get_movies_by_user(db, id)

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    return result

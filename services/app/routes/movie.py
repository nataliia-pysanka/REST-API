from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import SessionLocal, get_db
from app.schemas.movie import Movie
from app.domain.movie import DomainMovie
from app.crud.movie import CRUDMovie

movies_route = APIRouter()

domain_movie = DomainMovie(CRUDMovie)


@movies_route.get('/movies/', response_model=list[Movie])
def read_movies(offset: int = 0, limit: int = 10,
                db: Session = Depends(get_db)):
    movies = domain_movie.read_all(db, offset=offset, limit=limit)
    return movies


@movies_route.get("/movies/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = domain_movie.read(db, movie_id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
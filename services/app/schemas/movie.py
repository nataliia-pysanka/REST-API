from typing import Union, List, Optional, Any
from datetime import date, datetime
from pydantic import BaseModel, validator

from app.schemas.user import UserDB, UserCreate
from app.schemas.genre import GenreDB
from app.schemas.poster import PosterDB
from app.schemas.director import DirectorDB

from .validators import validate_value_alphabetical


class MovieBase(BaseModel):
    title: str

    # validators
    _normalize_title = validator('title',
                                allow_reuse=True)(validate_value_alphabetical)

    # @validator('title', pre=True)
    # def del_dot(cls, dot):
    #     if isinstance(dot, str):
    #         return ''
    #     return dot


class MovieCreate(MovieBase):
    description: Union[str, None] = None
    date_release: Union[date, None] = None
    rating: Union[float, None] = None
    id_genre: Union[List[Union[str, Any]], None] = None
    id_director: Union[str, Any, None] = None
    id_poster: Union[List[Union[str, Any]], None] = None
    id_user: Union[str, Any, None] = None

    # @validator('date_release')
    # def date_normal(cls, date_):
    #     if datetime(date_).year < datetime('1895-01-01').year:
    #         raise ValueError('Year should be bigger than 1895')
    #     return date_


class MovieUpdate(MovieBase):
    description: Union[str, None] = None
    date_release: Union[date, None] = None
    rating: Union[float, None] = None
    id_genre: Optional[List[Union[str, Any]]] = None
    id_director: Union[str, Any, None] = None
    id_poster: Optional[List[Union[str, Any]]] = None


class MovieDB(MovieBase):
    id: int
    title: str
    description: Union[str, None] = None
    date_release: Union[date, None] = None
    rating: Union[float, None] = None
    genre: Union[List[GenreDB], GenreDB, None] = None
    director: Optional[DirectorDB] = None
    poster: Union[List[PosterDB], PosterDB, None] = None
    user: UserDB
    
    class Config:
        orm_mode = True

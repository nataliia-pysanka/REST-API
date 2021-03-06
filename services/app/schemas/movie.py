"""Module for Movie pydantic models"""
from typing import Union, List, Optional, Any
from datetime import date, datetime
from pydantic import BaseModel, validator

from app.schemas.user import UserDB, UserCreate
from app.schemas.genre import GenreDB
from app.schemas.poster import PosterDB
from app.schemas.director import DirectorDB

from .validators import validate_value_alphabetical


class MovieBase(BaseModel):
    """Base pydantic model for Director"""
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
    """Create pydantic model for Movie"""
    description: Union[str, None] = None
    date_release: Union[date, None] = None
    rating: Union[float, None] = None
    id_genre: Union[Any, None] = None
    id_director: Union[str, Any, None] = None
    id_poster: Union[Any, None] = None
    id_user: Union[str, Any, None] = None

    # @validator('date_release')
    # def date_normal(cls, date_):
    #     if datetime(date_).year < datetime('1895-01-01').year:
    #         raise ValueError('Year should be bigger than 1895')
    #     return date_


class MovieUpdate(MovieBase):
    """Update pydantic model for Movie"""
    description: Union[str, None] = None
    date_release: Union[date, None] = None
    rating: Union[float, None] = None
    id_genre: Optional[Any] = None
    id_director: Union[str, Any, None] = None
    id_poster: Optional[Any] = None


class MovieDB(MovieBase):
    """ORM pydantic model for Movie"""
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

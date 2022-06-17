"""Module for Genre pydantic models"""
from pydantic import BaseModel, validator
from .validators import validate_value_alphabetical


class GenreBase(BaseModel):
    """Base pydantic model for Genre"""
    name: str

    # validators
    _normalize_name = validator('name',
                                allow_reuse=True)(validate_value_alphabetical)


class GenreCreate(GenreBase):
    """Create pydantic model for Genre"""
    name: str


class GenreUpdate(GenreBase):
    """Update pydantic model for Genre"""
    name: str


class GenreDB(GenreBase):
    """ORM pydantic model for Genre"""
    id: int
    name: str

    class Config:
        orm_mode = True

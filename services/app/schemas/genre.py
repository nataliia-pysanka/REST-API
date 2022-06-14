from typing import Union, List
from datetime import date
from pydantic import BaseModel, validator
from .validators import validate_value_alphabetical


class GenreBase(BaseModel):
    name: str

    # validators
    _normalize_name = validator('name',
                                allow_reuse=True)(validate_value_alphabetical)


class GenreCreate(GenreBase):
    name: str


class GenreUpdate(GenreBase):
    name: str


class GenreDB(GenreBase):
    id: int
    name: str

    class Config:
        orm_mode = True

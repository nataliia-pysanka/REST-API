"""Module for Director pydantic models"""
from typing import Union, Optional
from datetime import date
from pydantic import BaseModel, HttpUrl, validator
from .validators import validate_value_alphabetical


class DirectorBase(BaseModel):
    """Base pydantic model for Director"""
    name: str
    surname: str

    # validators
    _normalize_name = validator('name',
                                allow_reuse=True)(validate_value_alphabetical)
    _normalize_surname = validator('surname',
                                allow_reuse=True)(validate_value_alphabetical)


class DirectorCreate(DirectorBase):
    """Create pydantic model for Director"""
    date_birth: Union[date, None] = None
    wiki_url: Union[HttpUrl, None] = None

    @validator('wiki_url')
    def host_wiki_url(cls, url):
        if url.host not in ['en.wikipedia.org', '']:
            raise ValueError('URL should link to the wiki')
        return url


class DirectorUpdate(DirectorBase):
    """Update pydantic model for Director"""
    name: str
    surname: str
    date_birth: Union[date, str, None] = None
    wiki_url: Union[HttpUrl, None] = None


class DirectorDB(DirectorBase):
    """ORM pydantic model for Director"""
    id: int
    name: str
    surname: str
    date_birth: Optional[date] = None
    wiki_url: Union[HttpUrl, None] = None

    class Config:
        orm_mode = True

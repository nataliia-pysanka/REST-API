from typing import Union, Optional
from datetime import date
from pydantic import BaseModel, HttpUrl, validator
from .validators import validate_value_alphabetical


class DirectorBase(BaseModel):
    name: str
    surname: str

    # validators
    _normalize_name = validator('name',
                                allow_reuse=True)(validate_value_alphabetical)
    _normalize_surname = validator('surname',
                                allow_reuse=True)(validate_value_alphabetical)


class DirectorCreate(DirectorBase):
    date_birth: Union[date, None] = None
    wiki_url: Union[HttpUrl, None] = None

    @validator('wiki_url')
    def host_wiki_url(cls, url):
        if url.host not in ['en.wikipedia.org', '']:
            raise ValueError('URL should link to the wiki')
        return url


class DirectorUpdate(DirectorBase):
    name: str
    surname: str
    date_birth: Union[date, str, None] = None
    wiki_url: Union[HttpUrl, None] = None


class DirectorDB(DirectorBase):
    id: int
    name: str
    surname: str
    date_birth: Optional[date] = None
    wiki_url: Union[HttpUrl, None] = None

    class Config:
        orm_mode = True

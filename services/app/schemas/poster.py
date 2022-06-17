"""Module for Poster pydantic models"""
from pydantic import BaseModel, AnyUrl


class PosterBase(BaseModel):
    """Base pydantic model for Poster"""
    url: AnyUrl


class PosterCreate(PosterBase):
    """Create pydantic model for Poster"""
    pass


class PosterUpdate(PosterBase):
    """Update pydantic model for Poster"""
    pass


class PosterDB(PosterBase):
    """ORM pydantic model for Poster"""
    id: int
    url: AnyUrl

    class Config:
        orm_mode = True

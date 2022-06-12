from pydantic import BaseModel, AnyUrl


class PosterBase(BaseModel):
    url: AnyUrl


class PosterCreate(PosterBase):
    pass


class PosterUpdate(PosterBase):
    pass


class PosterDB(PosterBase):
    id: int
    url: AnyUrl

    class Config:
        orm_mode = True

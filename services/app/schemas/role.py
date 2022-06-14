from typing import Optional
from pydantic import BaseModel, validator
from .validators import validate_value_alphabetical


class RoleBase(BaseModel):
    name: str

    # validators
    _normalize_name = validator('name',
                                allow_reuse=True)(validate_value_alphabetical)


class RoleCreate(RoleBase):
    enabled: bool = True


class RoleUpdate(RoleBase):
    description: Optional[str] = None


class RoleDB(RoleBase):
    id: int
    name: str
    description: str = None
    enabled: bool

    class Config:
        orm_mode = True

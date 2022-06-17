"""Module for Role pydantic models"""
from typing import Optional
from pydantic import BaseModel, validator
from .validators import validate_value_alphabetical


class RoleBase(BaseModel):
    """Base pydantic model for Role"""
    name: str

    # validators
    _normalize_name = validator('name',
                                allow_reuse=True)(validate_value_alphabetical)


class RoleCreate(RoleBase):
    """Create pydantic model for Role"""
    description: Optional[str] = None
    enabled: bool = True


class RoleUpdate(RoleBase):
    """Update pydantic model for Role"""
    description: Optional[str] = None
    enabled: bool = True


class RoleDB(RoleBase):
    """ORM pydantic model for Role"""
    id: int
    name: str
    description: str = None
    enabled: bool

    class Config:
        orm_mode = True

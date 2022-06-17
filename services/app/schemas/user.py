"""Module for User pydantic models"""
from re import search as re_search
from typing import Union, Optional, Any
from datetime import date
from pydantic import BaseModel, SecretStr, validator
from app.schemas.role import RoleDB
from .validators import validate_value_alphabetical


class UserBase(BaseModel):
    """Base pydantic model for User"""
    nickname: str

    @validator('nickname')
    def nickname_must_not_contain_space(cls, name_):
        if ' ' in name_:
            raise ValueError("Mustn't contain a space")
        return name_.title()


class UserCreate(UserBase):
    """Create pydantic model for User"""
    password: str
    name: Union[str, None] = None
    surname: Union[str, None] = None
    date_birth: Union[date, None] = None
    date_registry: date
    id_role: Union[str, Any, None] = None

    # validators
    _normalize_name = validator('name',
                                allow_reuse=True)(validate_value_alphabetical)
    _normalize_surname = validator('surname',
                                allow_reuse=True)(validate_value_alphabetical)

    @validator('password')
    def passwords_match(cls, password_, values, **kwargs):
        if 'password' in values and password_ != values['password']:
            raise ValueError('Passwords do not match')
        return password_


class UserUpdate(UserBase):
    """Update pydantic model for User"""
    name: Union[str, None]
    surname: Union[str, None]
    date_birth: Union[date, None] = None
    id_role: Union[str, Any, None] = None

    @validator('name', 'surname')
    def name_alphanumeric(cls, name_):
        pattern = "[^a-zA-Z]"
        if re_search(pattern, name_):
            raise ValueError('Use letters for name and surname')
        return name_


class UserDB(UserBase):
    """ORM pydantic model for User"""
    id: int
    nickname: str
    name: str = None
    surname: str = None
    date_birth: Optional[date] = None
    date_registry: date
    role: RoleDB

    class Config:
        orm_mode = True
        json_encoders = {
            RoleDB: lambda a: f'{a.name} ({a.enabled})',
            'User': lambda u: f'{u.name} {u.surname} '
                              f'({u.date_birth})',
        }

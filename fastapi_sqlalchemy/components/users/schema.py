from pydantic import BaseModel
# from datetime import datetime
from enum import Enum
from uuid import UUID
# from typing import Any

## Note: Limit the use of inheritance, and make schemas as direct as you can.abs

class Role(str, Enum):
    DBA = 'DBA'
    Analytics = 'Analytics'
    Management = 'Management'

class User(BaseModel):
    name: str
    password: str
    roles: list[Role]

class UserBaseRes(BaseModel):
    id: UUID
    name: str
    roles: list[Role]

class UserSignupReq(User):
    pass


class UserSignupRes(BaseModel):
    user: UserBaseRes
    access_token: str
    # created_at: datetime
    # updated_at: datetime


class UserLoginReq(BaseModel):
    name: str
    password: str

class UserLoginRes(BaseModel):
    user: UserBaseRes
    access_token: str

class UserUpdateReq(BaseModel):
    name: str | None = None
    password: str | None = None
    roles: list[Role] | None = None

class UserUpdateRes(BaseModel):
    pass

class UserDeleteReq(BaseModel):
    pass

class UserDeleteRes(BaseModel):
    pass
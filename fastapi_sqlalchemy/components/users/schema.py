from pydantic import BaseModel
# from datetime import datetime
from enum import Enum
from uuid import UUID

## Note: Limit the use of inheritance, and make schemas as direct as you can.abs

class Role(Enum):
    DBA = 'DBA'
    Analytics = 'Analytics'
    Management = 'Management'

class User(BaseModel):
    name: str
    password: str
    roles: list[Role]


class UserSignupReq(User):
    pass


class UserSignupRes(BaseModel):
    id: UUID
    name: str
    roles: list[Role]
    # created_at: datetime
    # updated_at: datetime


class UserLoginReq(BaseModel):
    name: str
    password: str

class UserLoginRes(BaseModel):
    id: UUID
    name: str
    roles: list[Role]

class UserUpdateReq(BaseModel):
    name: str | None = None
    password: str | None = None
    roles: list[Role] | None = None

class UserUpdateRes(BaseModel):
    pass
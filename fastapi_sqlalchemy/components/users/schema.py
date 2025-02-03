from pydantic import BaseModel, Field
# from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import Annotated

## Note: Limit the use of inheritance, and make schemas as direct as you can.abs

class Role(str, Enum):
    DBA = 'DBA'
    Analytics = 'Analytics'
    Management = 'Management'

class User(BaseModel):
    name: Annotated[str, Field(min_length=4, max_length=128, examples=["Ron Gyie"])]
    password: Annotated[str, Field(min_length=8, max_length=128, examples=["*P@ssword1*"])]
    # Password Pattern validation, should be used in Signup & Update Requests only.
    # password: Annotated[str, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])] 
    roles: Annotated[list[Role], Field(min_length=1,max_length=3,examples=[["DBA", "Analytics"]])]

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
    name: Annotated[str, Field(min_length=4, max_length=128, examples=["Ron Gyie"])]
    password: Annotated[str, Field(min_length=8, max_length=128, examples=["*P@ssword1*"])]

class UserLoginRes(BaseModel):
    user: UserBaseRes
    access_token: str

class UserUpdateReq(BaseModel):
    name: Annotated[str, Field(min_length=4, max_length=128, examples=["Ron Gyie"])] | None = None
    password: Annotated[str, Field(min_length=8, max_length=128, examples=["*P@ssword1*"])] | None = None
    roles: Annotated[list[Role], Field(min_length=1,max_length=3,examples=[["DBA", "Analytics"]])] | None = None

class UserUpdateRes(BaseModel):
    pass

class UserDeleteReq(BaseModel):
    pass

class UserDeleteRes(BaseModel):
    pass
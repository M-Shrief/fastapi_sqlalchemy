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


class UserSignupRes(User):
    id: UUID
    # created_at: datetime
    # updated_at: datetime


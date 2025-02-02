import bcrypt
import jwt
from typing import Any
from datetime import UTC, datetime, timedelta
### 
from fastapi_sqlalchemy.config import JWT
from fastapi_sqlalchemy.components.users import schema

def hash_password(password: str) -> str:
    hashed_password: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    return hashed_password.decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_jwt(user: schema.UserBaseRes)->str:
    permissions = create_permissions(user.roles)
    payload = {
        "user": {
            "id": str(user.id),
            "name": user.name,
            },
        "permissions": permissions
    }
    time: datetime = datetime.now(UTC).replace(tzinfo=None)
    payload["iat"]= time # Issued at {time}
    payload["exp"]= time + timedelta(minutes= 60 * 2) # Expire after 2 hours

    token: str = jwt.encode(
        payload=payload,
        key=JWT["private"],
        algorithm="RS256"
        )

    return token

def verify_jwt(authorization_header: str, only_authorized_for: list[str])->(Any | None, bool):
    token = authorization_header[7:]
    try:
        payload = jwt.decode(
            jwt=token,
            key=JWT["public"],
            algorithms=["RS256"]
            )
        expire_timepstamp = datetime.fromtimestamp(payload["exp"]).replace(tzinfo=None)
        current_timepstamp = datetime.now(UTC).replace(tzinfo=None)
        # if the expire date is smaller than the current time (i.e. has passed), then it's not authorized 
        if expire_timepstamp < current_timepstamp:
            return payload, False

        isAuthorized: bool = is_authorized(onlyAuthorizedFor=only_authorized_for, permissions=payload["permissions"])
        if isAuthorized is False:
            return payload, False

        return payload, True
    except jwt.DecodeError:
        return None, False

# def create_jwtpayload():
#     pass

def create_permissions(roles: list[schema.Role])->list[str]:
    permission: list[str] = []
    for role in roles:
        permission.append(role + ":read") # read permission
        permission.append(role + ":write") # write permission

    return permission

def is_authorized(onlyAuthorizedFor: list[str], permissions: list[str]):
    isAuthorized: bool = False

    for permission in permissions:
        try:
            onlyAuthorizedFor.index(permission)
            # if it didn't raise an error
            isAuthorized = True
            break
        except ValueError:
            continue

    return isAuthorized
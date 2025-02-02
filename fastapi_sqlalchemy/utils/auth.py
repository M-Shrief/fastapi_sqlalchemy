import bcrypt
import jwt
from typing import Any
from datetime import UTC, datetime, timedelta
import json
### 
from fastapi_sqlalchemy.config import JWT
from fastapi_sqlalchemy.components.users import schema

def hash_password(password: str) -> str:
    hashed_password: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    return hashed_password.decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_access_token(user: schema.UserBaseRes)->str:
    payload = {
        "user": {
            "id": str(user.id),
            "name": user.name,
            "roles": user.roles
            }
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

def verify_access_token(token: str)->(Any | None, bool):
    try:
        payload = jwt.decode(
            token=token,
            key=JWT["public"],
            algorithms=["RS256"]
            )

        return payload, True
    except jwt.DecodeError:
        return None, False
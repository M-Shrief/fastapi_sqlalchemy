from fastapi import APIRouter, HTTPException, status, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Annotated
###
from fastapi_sqlalchemy.components.users import schema
from fastapi_sqlalchemy.database.index import get_db
from fastapi_sqlalchemy.database.models import User
from fastapi_sqlalchemy.utils.auth import hash_password, verify_password, create_jwt, verify_jwt


router = APIRouter(tags=["Users"])



@router.post(
    "/users/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.UserSignupRes,
    response_model_exclude_none=True
    )
async def signup(user: schema.UserSignupReq, db: AsyncSession = Depends(get_db)):
    new_user = User(**user.model_dump())
    new_user.password = hash_password(new_user.password)
    try: 
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        user = schema.UserBaseRes(id=new_user.id, name=new_user.name, roles=new_user.roles)
        access_token = create_jwt(user)
        return schema.UserSignupRes(user=user, access_token=access_token)
    except Exception as e: ## need effective error handling here
        await db.rollback()
        if "psycopg.errors.UniqueViolation" in str(e):
            detail_msg = "Name's already taken"
            raise HTTPException(status.HTTP_409_CONFLICT, detail=detail_msg)
        else:
            detail_msg = "An error occurred while signing up, try again later."
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=detail_msg)

@router.post(
    "/users/login",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schema.UserLoginRes,
    response_model_exclude_none=True
)
async def login(user: schema.UserLoginReq, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(User).where(User.name == user.name) ## need to select required fields only.
        res =  await db.execute(statement=stmt)
        existing_user: User = res.scalar()
    except Exception:
        detail_msg = "An error occurred while loggin in, try again later."
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=detail_msg)


    base_err = "User's name or password is incorrect."
    if existing_user: # User exist in DB

        if verify_password(user.password, existing_user.password) is False: # if password is incorrect.
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=base_err)

        
        user = schema.UserBaseRes(id=existing_user.id, name=existing_user.name, roles=existing_user.roles)
        access_token = create_jwt(user)
        return schema.UserLoginRes(user=user, access_token=access_token)

    else:
        # User doesn't exist
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=base_err)


@router.put(
    "/users/me",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schema.UserUpdateRes,
    response_model_exclude_none=True,
)
async def update_user(new_user_data: schema.UserUpdateReq, Authorization: Annotated[str | None, Header()] = None, db: AsyncSession = Depends(get_db)):
    if Authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Action Not Authorized")

    only_authorized_for: list[str] = [
        schema.Role.DBA + ":write",
        schema.Role.Management + ":write",
        schema.Role.Analytics + ":write"
    ]

    payload, verified = verify_jwt(authorization_header=Authorization, only_authorized_for=only_authorized_for)
    if verified is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Action Not Authorized")
    
    user = payload["user"] # getting user data from payload
    try:
        hashed_password: str = ""
        if new_user_data.password is not None:
            hashed_password = hash_password(new_user_data.password)

        stmt = select(User).where(User.id == user["id"]) 
        res =  await db.execute(statement=stmt)
        existing_user: User = res.scalar()

        if existing_user: # User exist in DB

            if new_user_data.name is not None:
                existing_user.name = new_user_data.name

            if new_user_data.password is not None:
                hashed_password = hash_password(new_user_data.password)
                existing_user.password = hashed_password

            if new_user_data.roles is not None:
                existing_user.roles = new_user_data.roles

            await db.commit()
            return schema.UserUpdateRes()
        else:
            # User doesn't exist
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User doesn't exists")
    except Exception as e:
        print(e)
        detail_msg = "An error occurred while updating the user, try again later."
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=detail_msg)

@router.delete(
    "/users/me",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schema.UserDeleteReq,
    response_model_exclude_none=True,
)
async def delete_user(Authorization: Annotated[str | None, Header()] = None, db: AsyncSession = Depends(get_db)):
    if Authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Action Not Authorized")

    only_authorized_for: list[str] = [
        schema.Role.DBA + ":write",
        schema.Role.Management + ":write",
        schema.Role.Analytics + ":write"
    ]

    payload, verified = verify_jwt(authorization_header=Authorization, only_authorized_for=only_authorized_for)
    if verified is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Action Not Authorized")
    
    user = payload["user"] # getting user data from payload
    
    stmt = delete(User).where(User.id == user["id"])
    await db.execute(statement=stmt)
    await db.commit()

    return schema.UserDeleteRes()
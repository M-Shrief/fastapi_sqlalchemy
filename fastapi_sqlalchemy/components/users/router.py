from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
###
from fastapi_sqlalchemy.components.users import schema
from fastapi_sqlalchemy.database.index import get_db
from fastapi_sqlalchemy.database.models import User


router = APIRouter(tags=["Users"])



@router.post(
    "/api/users",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.UserSignupRes,
    response_model_exclude_none=True
    )
async def signup(user: schema.UserSignupReq, db: AsyncSession = Depends(get_db)):
    new_user = User(**user.model_dump())
    try: 
        print(new_user.name, new_user.password, new_user.roles)
        db.add(new_user)
        print("Added")
        await db.commit()
        print("commited")
        await db.refresh(new_user)
        print("Refreshed User: ", new_user)
        return new_user
    except Exception as e: ## need effective error handling here
        await db.rollback()
        print(e)
        return
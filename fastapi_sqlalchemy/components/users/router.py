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
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e: ## need effective error handling here
        await db.rollback()
        if "psycopg.errors.UniqueViolation" in str(e):
            detail_msg = "Name's already taken"
            raise HTTPException(status.HTTP_409_CONFLICT, detail=detail_msg)
        else:
            detail_msg = "An error occurred while signing up"
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=detail_msg)

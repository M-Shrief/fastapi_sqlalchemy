from fastapi import FastAPI
###
from fastapi_sqlalchemy.database.index import lifespan
from fastapi_sqlalchemy.components.users.router import router as user_router

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def homepage():
    return {"message": "Hello World!"}


app.include_router(user_router, prefix="/api")
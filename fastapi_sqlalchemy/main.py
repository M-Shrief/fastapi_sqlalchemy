from fastapi import FastAPI
###
from fastapi_sqlalchemy.database.index import lifespan

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def homepage():
    return {"message": "Hello World!"}
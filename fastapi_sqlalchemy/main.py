from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
###
from fastapi_sqlalchemy.database.index import lifespan
from fastapi_sqlalchemy.components.users.router import router as user_router
from fastapi_sqlalchemy.utils.logger import logger

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
    compresslevel=5
)

@app.get("/")
async def homepage():
    logger.info("21412", arr=["aa", "bb"], dic={"name1": "Name1"})
    return {"message": "Hello World!"}


app.include_router(user_router, prefix="/api")
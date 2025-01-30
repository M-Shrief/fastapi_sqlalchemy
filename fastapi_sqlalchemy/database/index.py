from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.engine import URL 
#####
from fastapi_sqlalchemy.config import DB
from fastapi_sqlalchemy.database.models import Base

db_url = URL.create(
    drivername="postgresql+psycopg",
    # drivername="postgresql",
    username=DB.get('user'),
    password=DB.get('password'),
    host=DB['host'],
    database=DB.get('name'),
    port=DB.get('port')
)


engine = create_async_engine(db_url)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        pass
    yield

# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

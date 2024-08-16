from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from logger import get_logger

logger = get_logger()

Base = declarative_base()
engine = create_async_engine("mariadb+asyncmy://python:python@127.0.0.1:33306/python?charset=utf8mb4", echo=True, pool_pre_ping=True, pool_recycle=280)
async_session = sessionmaker(engine, expire_on_commit=False, autocommit=False, class_=AsyncSession)

async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_database():
    await engine.dispose()

async def get_async_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
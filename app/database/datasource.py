from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models.common import Base
from logger import get_logger

logger = get_logger()

engine = create_async_engine("mariadb+asyncmy://python:python@127.0.0.1:33306/python?charset=utf8mb4", echo=True, pool_pre_ping=True, pool_recycle=280)
async_session = sessionmaker(engine, expire_on_commit=False, autocommit=False, class_=AsyncSession)

async def init_database():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        # alembic 에게 이관
        pass

async def close_database():
    await engine.dispose()

async def get_async_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings
from typing import AsyncGenerator

engine = create_async_engine(settings.DATABASE_URL,echo=True)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/my_db"

AsyncSessionLocal = async_sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine,
                                       class_=AsyncSession,
                                       expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocal() as session:
        yield session

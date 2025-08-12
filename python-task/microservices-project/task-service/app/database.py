import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Database URL from environment variable
DATABASE_URL = os.getenv("DB_URL", "postgresql+asyncpg://postgres:password@localhost:5433/taskdb")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session maker
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """Dependency to get database session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

            
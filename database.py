import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Load environment variables
load_dotenv()

# Get the URL (ensure your .env has DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the async engine
engine = create_async_engine(DATABASE_URL)

# Create the async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)

# Async dependency generator using 'async with' for safe cleanup
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

# Base class for models
class Base(DeclarativeBase):
    pass
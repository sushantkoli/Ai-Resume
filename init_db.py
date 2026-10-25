import asyncio
from sqlalchemy import text
from database import Base, engine
import models  # This is crucial so SQLAlchemy knows about the Resume class

async def init_models():
    async with engine.begin() as conn:
        # Enable the pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        
        # Create all tables defined in models.py
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from src.books.models import Book
from src.config import Config


engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
    connect_args={
        "ssl": True  
    }
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

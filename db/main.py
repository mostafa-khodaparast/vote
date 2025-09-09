from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
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
        result = await conn.execute(text("SELECT 'hello';"))
        print(result.all())

from fastapi import FastAPI
from contextlib import asynccontextmanager
import sys

from src.books.routes import book_router
from src.auth.routes import auth_router
from src.db.main import init_db


version = "v1"


def is_running_under_alembic() -> bool:
    return any("alembic" in arg for arg in sys.argv)


@asynccontextmanager
async def life_span(app: FastAPI):
    if not is_running_under_alembic():
        await init_db()
    yield


app = FastAPI(
    title="bookly",
    description="A rest api for a book review web service",
    version=version,
    lifespan=life_span,
)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])

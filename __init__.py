from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.routes import book_router
from src.db.main import init_db


version = "v1"


@asynccontextmanager
async def life_span(app:FastAPI):
    print("server started mostafa.......")
    await init_db()
    yield
    print("server stopped mmmmmssoooooooooo")


app = FastAPI(
    title= "bookly",
    description="A rest api for a book review web service",
    version = version,
    lifespan= life_span
)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])

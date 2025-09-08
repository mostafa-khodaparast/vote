from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List

from src.books.book_data import books
from src.books.schemas import Book


book_router = APIRouter()


@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books


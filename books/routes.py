from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.books.service import BookService
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])


@book_router.get("/", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
    _: bool = Depends(role_checker),
):
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
    _: bool = Depends(role_checker),
) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_id}", response_model=Book)
async def get_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
    _: bool = Depends(role_checker),
) -> dict:
    book = await book_service.get_book(book_id, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book not found"
        )


@book_router.patch("/{book_id}", response_model=Book)
async def update_book(
    book_id: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
    _: bool = Depends(role_checker),
) -> dict:
    update_book = await book_service.update_book(book_id, book_update_data, session)
    if update_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book not found"
        )
    else:
        return update_book


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
    _: bool = Depends(role_checker),
):
    deleted_book = await book_service.delete_book(book_id, session)
    if deleted_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book not found"
        )
    else:
        return {}

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_admin_user, get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.schemas.borrow_record import BorrowRecordResponse
from app.services.book_service import book_service
from app.services.borrow_service import borrow_service

router = APIRouter()


@router.get("/", response_model=list[BookResponse])
async def list_books(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await book_service.get_all(db)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await book_service.get_by_id(db, book_id)


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    data: BookCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    return await book_service.create_book(db, data)


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    data: BookUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    return await book_service.update_book(db, book_id, data)


@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    await book_service.delete_book(db, book_id)


@router.post("/{book_id}/borrow", response_model=BorrowRecordResponse)
async def borrow_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await book_service.borrow_book(db, book_id, current_user.id)


@router.post("/{book_id}/return", response_model=BorrowRecordResponse)
async def return_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await book_service.return_book(db, book_id, current_user.id)


@router.get("/{book_id}/records", response_model=list[BorrowRecordResponse])
async def get_book_records(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await borrow_service.get_book_records(db, book_id)

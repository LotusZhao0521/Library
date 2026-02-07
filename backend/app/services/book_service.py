from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book
from app.models.borrow_record import BorrowRecord
from app.repositories.book_repository import book_repository
from app.repositories.borrow_repository import borrow_repository
from app.schemas.book import BookCreate, BookUpdate


class BookService:
    async def create_book(self, db: AsyncSession, data: BookCreate) -> Book:
        existing = await book_repository.get_by_book_no(db, data.book_no)
        if existing:
            raise HTTPException(status_code=400, detail="图书编号已存在")
        book = Book(
            book_no=data.book_no,
            title=data.title,
            author=data.author,
            isbn=data.isbn,
            publisher=data.publisher,
        )
        return await book_repository.create(db, book)

    async def update_book(
        self, db: AsyncSession, book_id: int, data: BookUpdate
    ) -> Book:
        book = await book_repository.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="图书不存在")
        if data.book_no and data.book_no != book.book_no:
            existing = await book_repository.get_by_book_no(db, data.book_no)
            if existing:
                raise HTTPException(status_code=400, detail="图书编号已存在")
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)
        return await book_repository.update(db, book)

    async def delete_book(self, db: AsyncSession, book_id: int) -> None:
        book = await book_repository.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="图书不存在")
        if book.status == "borrowed":
            raise HTTPException(status_code=400, detail="图书正在借阅中，无法删除")
        await book_repository.delete(db, book)

    async def get_all(self, db: AsyncSession) -> list[Book]:
        return await book_repository.get_all(db)

    async def get_by_id(self, db: AsyncSession, book_id: int) -> Book:
        book = await book_repository.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="图书不存在")
        return book

    async def borrow_book(
        self, db: AsyncSession, book_id: int, user_id: int
    ) -> BorrowRecord:
        book = await book_repository.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="图书不存在")
        if book.status == "borrowed":
            raise HTTPException(status_code=400, detail="图书已被借出")
        # Check borrow limit: max 1 book per user
        active_borrow = await borrow_repository.get_active_by_user(db, user_id)
        if active_borrow:
            raise HTTPException(
                status_code=400, detail="您已借阅一本图书，请归还后再借阅"
            )
        # Create borrow record
        record = BorrowRecord(book_id=book_id, user_id=user_id)
        record = await borrow_repository.create(db, record)
        # Update book status
        book.status = "borrowed"
        await book_repository.update(db, book)
        return record

    async def return_book(
        self, db: AsyncSession, book_id: int, user_id: int
    ) -> BorrowRecord:
        book = await book_repository.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="图书不存在")
        active = await borrow_repository.get_active_by_book(db, book_id)
        if not active or active.user_id != user_id:
            raise HTTPException(status_code=400, detail="您未借阅此图书")
        active.return_time = datetime.utcnow()
        await borrow_repository.update(db, active)
        book.status = "available"
        await book_repository.update(db, book)
        return active


book_service = BookService()

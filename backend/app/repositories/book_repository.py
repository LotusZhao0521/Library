from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book


class BookRepository:
    async def get_by_id(self, db: AsyncSession, book_id: int) -> Book | None:
        result = await db.execute(select(Book).where(Book.id == book_id))
        return result.scalars().first()

    async def get_by_book_no(self, db: AsyncSession, book_no: str) -> Book | None:
        result = await db.execute(select(Book).where(Book.book_no == book_no))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> list[Book]:
        result = await db.execute(select(Book).order_by(Book.created_at.desc()))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, book: Book) -> Book:
        db.add(book)
        await db.flush()
        await db.refresh(book)
        return book

    async def update(self, db: AsyncSession, book: Book) -> Book:
        await db.flush()
        await db.refresh(book)
        return book

    async def delete(self, db: AsyncSession, book: Book) -> None:
        await db.delete(book)
        await db.flush()


book_repository = BookRepository()

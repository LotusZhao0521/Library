from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.borrow_record import BorrowRecord


class BorrowRepository:
    async def get_by_id(self, db: AsyncSession, record_id: int) -> BorrowRecord | None:
        result = await db.execute(
            select(BorrowRecord).where(BorrowRecord.id == record_id)
        )
        return result.scalars().first()

    async def get_active_by_user(
        self, db: AsyncSession, user_id: int
    ) -> BorrowRecord | None:
        result = await db.execute(
            select(BorrowRecord).where(
                and_(
                    BorrowRecord.user_id == user_id,
                    BorrowRecord.return_time.is_(None),
                )
            )
        )
        return result.scalars().first()

    async def get_active_by_book(
        self, db: AsyncSession, book_id: int
    ) -> BorrowRecord | None:
        result = await db.execute(
            select(BorrowRecord).where(
                and_(
                    BorrowRecord.book_id == book_id,
                    BorrowRecord.return_time.is_(None),
                )
            )
        )
        return result.scalars().first()

    async def get_by_user(self, db: AsyncSession, user_id: int) -> list[BorrowRecord]:
        result = await db.execute(
            select(BorrowRecord)
            .where(BorrowRecord.user_id == user_id)
            .order_by(BorrowRecord.borrow_time.desc())
        )
        return list(result.scalars().all())

    async def get_by_book(self, db: AsyncSession, book_id: int) -> list[BorrowRecord]:
        result = await db.execute(
            select(BorrowRecord)
            .where(BorrowRecord.book_id == book_id)
            .order_by(BorrowRecord.borrow_time.desc())
        )
        return list(result.scalars().all())

    async def get_all(self, db: AsyncSession) -> list[BorrowRecord]:
        result = await db.execute(
            select(BorrowRecord).order_by(BorrowRecord.borrow_time.desc())
        )
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, record: BorrowRecord) -> BorrowRecord:
        db.add(record)
        await db.flush()
        await db.refresh(record)
        return record

    async def update(self, db: AsyncSession, record: BorrowRecord) -> BorrowRecord:
        await db.flush()
        await db.refresh(record)
        return record


borrow_repository = BorrowRepository()

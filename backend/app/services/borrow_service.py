from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.borrow_record import BorrowRecord
from app.repositories.borrow_repository import borrow_repository


class BorrowService:
    async def get_user_records(
        self, db: AsyncSession, user_id: int
    ) -> list[BorrowRecord]:
        return await borrow_repository.get_by_user(db, user_id)

    async def get_book_records(
        self, db: AsyncSession, book_id: int
    ) -> list[BorrowRecord]:
        return await borrow_repository.get_by_book(db, book_id)

    async def get_all_records(self, db: AsyncSession) -> list[BorrowRecord]:
        return await borrow_repository.get_all(db)

    async def update_note(
        self, db: AsyncSession, record_id: int, user_id: int, note: str
    ) -> BorrowRecord:
        record = await borrow_repository.get_by_id(db, record_id)
        if not record:
            raise HTTPException(status_code=404, detail="借阅记录不存在")
        if record.user_id != user_id:
            raise HTTPException(status_code=403, detail="无权修改此记录")
        record.note = note
        return await borrow_repository.update(db, record)


borrow_service = BorrowService()

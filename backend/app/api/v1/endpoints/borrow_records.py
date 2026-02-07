from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.borrow_record import BorrowRecordResponse, NoteUpdate
from app.services.borrow_service import borrow_service

router = APIRouter()


@router.get("/", response_model=list[BorrowRecordResponse])
async def list_my_records(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await borrow_service.get_user_records(db, current_user.id)


@router.put("/{record_id}/note", response_model=BorrowRecordResponse)
async def update_note(
    record_id: int,
    data: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await borrow_service.update_note(db, record_id, current_user.id, data.note)

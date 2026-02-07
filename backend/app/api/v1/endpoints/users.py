from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_admin_user, get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import PasswordChange, RoleUpdate, UserCreate, UserResponse
from app.services.user_service import user_service

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me/password", response_model=UserResponse)
async def change_password(
    data: PasswordChange,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.change_password(
        db, current_user, data.old_password, data.new_password
    )


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    return await user_service.create_user(db, data)


@router.get("/", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    return await user_service.get_all(db)


@router.put("/{user_id}/role", response_model=UserResponse)
async def update_role(
    user_id: int,
    data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    return await user_service.update_role(db, user_id, data.role)

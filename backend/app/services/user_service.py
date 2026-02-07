from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate


class UserService:
    async def create_user(self, db: AsyncSession, data: UserCreate) -> User:
        existing = await user_repository.get_by_username(db, data.username)
        if existing:
            raise HTTPException(status_code=400, detail="用户名已存在")
        if data.role not in ("admin", "user"):
            raise HTTPException(status_code=400, detail="无效的角色")
        user = User(
            username=data.username,
            hashed_password=get_password_hash(data.password),
            role=data.role,
        )
        return await user_repository.create(db, user)

    async def get_all(self, db: AsyncSession) -> list[User]:
        return await user_repository.get_all(db)

    async def change_password(
        self, db: AsyncSession, user: User, old_password: str, new_password: str
    ) -> User:
        if not verify_password(old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="原密码错误")
        user.hashed_password = get_password_hash(new_password)
        return await user_repository.update(db, user)

    async def update_role(self, db: AsyncSession, user_id: int, role: str) -> User:
        if role not in ("admin", "user"):
            raise HTTPException(status_code=400, detail="无效的角色")
        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        user.role = role
        return await user_repository.update(db, user)


user_service = UserService()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.entities.user import User
from app.schemas.user_schemas import UserCreate, UserRead
from typing import Optional, List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreate) -> UserRead:
        hashed_password = UserService.hash_password(user.password)

        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return UserRead.from_orm(db_user)
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[UserRead]:
        result = await db.execute(select(User).where(User.email == email))
        db_user = result.scalars().first()
        if db_user:
            return UserRead.from_orm(db_user)
        return None
    
    @staticmethod
    async def get_user_by_email_raw(db: AsyncSession, email: str) -> User:
        """Use this function for login only."""
        result = await db.execute(select(User).where(User.email == email))
        db_user = result.scalars().first()
        return db_user
    
    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> Optional[UserRead]:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if db_user:
            return UserRead.from_orm(db_user)
        return None
    
    @staticmethod
    async def get_all_users(db: AsyncSession) -> List[UserRead]:
        result = await db.execute(select(User))
        users = result.scalars().all()
        return [UserRead.from_orm(user) for user in users]
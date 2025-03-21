from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user_schemas import UserCreate, UserRead
from app.services.user_service import UserService
from app.database.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    created_user = await user_service.create_user(user)
    return created_user

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.get("/", response_model=List[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    users = await user_service.get_all_users()
    return users
from fastapi import APIRouter, Depends

from dependencies import get_current_user
from models.users import User
from schemas.users import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    """Отримання даних поточного авторизованого користувача."""
    return current_user
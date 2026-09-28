from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.security import get_password_hash, verify_password, create_access_token
from models.users import User
from repository.users import UserRepository, user_repository
from schemas.users import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, db: Session, user_in: UserCreate) -> User:
        """Реєстрація нового користувача."""
        # 1. Перевіряємо, чи немає користувача з таким email
        existing_user = self.repo.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Користувач із таким email вже існує."
            )

        # 2. Хешуємо пароль
        hashed_pwd = get_password_hash(user_in.password)

        # 3. Зберігаємо в БД через репозиторій
        return self.repo.create(
            db,
            email=user_in.email,
            name=user_in.name,
            hashed_password=hashed_pwd
        )

    def authenticate_user(self, db: Session, email: str, password: str) -> str:
        """Перевірка пароля та генерація JWT токена при входу."""
        user = self.repo.get_by_email(db, email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невірний email або пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Акаунт деактивовано."
            )

        # Повертаємо JWT токен із UUID користувача в полі sub
        return create_access_token(subject=user.id)


# Екземпляр сервісу
user_service = UserService(repo=user_repository)
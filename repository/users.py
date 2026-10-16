from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from models.users import User

class UserRepository:
    def get_by_id(self, db: Session, user_id: UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, email: str, name: str, hashed_password: str) -> User:
        db_user = User(
            email=email,
            name=name,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

user_repository = UserRepository()
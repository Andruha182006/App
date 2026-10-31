import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    department: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        unique=True,
        nullable=True,
    )

    courses = relationship(
        "Course",
        back_populates="teachers",
        passive_deletes=True,
    )
    schedules = relationship(
        "Schedule",
        back_populates="teachers",
        passive_deletes=True,
    )
    tasks = relationship(
        "Task",
        back_populates="teachers",
        passive_deletes=True,
    )

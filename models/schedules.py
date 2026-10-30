from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Schedule(Base):
    __tablename__ = 'schedules'

    id: Mapped[int] = mapped_column(primary_key=True)
    group: Mapped[str] = mapped_column(String(50))
    room: Mapped[int] = mapped_column()
    course_id: Mapped[int] = mapped_column(
        ForeignKey('courses.id'),
        nullable=False,
        index=True,
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey('teachers.id'),
        nullable=False,
        index=True,
    )

    courses = relationship("Course", back_populates="schedules")
    teachers = relationship("Teacher", back_populates="schedules")

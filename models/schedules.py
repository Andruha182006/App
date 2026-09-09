from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from core.database import Base

class Schedule(Base):
    __tablename__ = 'schedules'

    id: Mapped[int]=mapped_column(primary_key=True,unique=True)
    group:Mapped[str]=mapped_column(String(50))
    room:Mapped[int]=mapped_column()
    course_id:Mapped[int]=mapped_column(ForeignKey('courses.id'),nullable=False)
    teacher_id:Mapped[int]=mapped_column(ForeignKey('teachers.id'),nullable=False)

    course = relationship("Course", back_populates="schedules")
    teacher = relationship("Teacher", back_populates="schedules")
from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from core.database import Base

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str]=mapped_column(String(100))
    student_id: Mapped[int]=mapped_column(ForeignKey('students.id'),nullable=False)
    teacher_id: Mapped[int]=mapped_column(ForeignKey('teachers.id'),nullable=False)

    student = relationship("Student", back_populates="tasks")
    teacher = relationship("Teacher", back_populates="tasks")
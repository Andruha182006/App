from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from core.database import Base

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str]=mapped_column(String(100))
    student_id: Mapped[int]=mapped_column(ForeignKey=True)
    teacher_id: Mapped[int]=mapped_column(ForeignKey=True)
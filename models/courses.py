from sqlalchemy import String,ForeignKey
<<<<<<< HEAD
from sqlalchemy.orm import Mapped,mapped_column,relationship
=======
from sqlalchemy.orm import Mapped,mapped_column
>>>>>>> feature/repository
from core.database import Base


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(50))
    credits:Mapped[int]=mapped_column()
<<<<<<< HEAD
    teacher_id:Mapped[int]=mapped_column(ForeignKey('teachers.id'),nullable=False)
=======

    teacher_id:Mapped[int]=mapped_column(ForeignKey('teachers.id'))
>>>>>>> feature/repository

    teachers = relationship("Teacher", back_populates="courses")
    schedules = relationship("Schedule", back_populates="courses")
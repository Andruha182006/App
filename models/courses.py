from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from core.database import Base


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(50))
    credits:Mapped[int]=mapped_column()
    teacher_id:Mapped[int]=mapped_column(ForeignKey('teachers.id'),nullable=False)

    teacher = relationship("Teacher", back_populates="courses")
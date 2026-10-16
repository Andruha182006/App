from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from core.database import Base

class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int]=mapped_column(primary_key=True,index=True)
    name:Mapped[str]=mapped_column(String(25),nullable=False)
    age:Mapped[int]=mapped_column(nullable=False)
    email:Mapped[str]=mapped_column(String(100),unique=True,index=True,nullable=False)

    tasks = relationship("Task", back_populates="students")
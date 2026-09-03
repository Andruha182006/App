from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from core.database import Base

class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(50))
    age:Mapped[int]=mapped_column()
    email:Mapped[str]=mapped_column(String(100),unique=True,index=True)

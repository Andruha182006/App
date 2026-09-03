from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from core.database import Base

class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(50))
    credits:Mapped[int]=mapped_column()
    teacher_id:Mapped[int]=mapped_column(ForeignKey=True)


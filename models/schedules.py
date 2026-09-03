from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from core.database import Base

class Schedule(Base):
    __tablename__ = 'schedules'

    id: Mapped[int]=mapped_column(primary_key=True)
    group:Mapped[str]=mapped_column(String(50))
    room:Mapped[int]=mapped_column()
    course_id:Mapped[int]=mapped_column(ForeignKey=True)
    teacher_id:Mapped[int]=mapped_column(ForeignKey=True)

import uuid
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,String,Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from core.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID]=mapped_column(PG_UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name:Mapped[str|None] = mapped_column(String(100), nullable=True)
    email:Mapped[str]=mapped_column(String(255),unique=True,index=True,nullable=False)
    hashed_password:Mapped[str] = mapped_column(String(255),nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean,default=False,nullable=False)
    is_superuser:Mapped[bool] = mapped_column(Boolean,default=False,nullable=False)
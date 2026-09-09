
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,BigInteger,DateTime,func

from datetime import datetime

class Base(DeclarativeBase):
    pass

class Organization(Base):
    __tablename__ = "organizations"

    id:Mapped[int] = mapped_column(BigInteger,primary_key = True)
    name:Mapped[str] = mapped_column(String(255),nullable= False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default = func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default = func.now(),onupdate = func.now(),nullable=False)
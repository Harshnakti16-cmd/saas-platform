
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,BigInteger,DateTime,func,ForeignKey,UniqueConstraint,Date,Text
from datetime import datetime,date

class Base(DeclarativeBase):
    pass

class Organization(Base):
    __tablename__ = "organizations"

    id:Mapped[int] = mapped_column(BigInteger,primary_key = True)
    name:Mapped[str] = mapped_column(String(255),nullable= False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default = func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default = func.now(),onupdate = func.now(),nullable=False)


class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(BigInteger,primary_key =True)
    name:Mapped[str] = mapped_column(String(255),nullable=False)
    email:Mapped[str] = mapped_column(String(255),nullable=False,unique = True)
    password_hash:Mapped[str] = mapped_column(Text,nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default= func.now(),nullable=False)
    updated_at:Mapped[datetime] =mapped_column(DateTime(timezone=True),default = func.now(),onupdate=func.now(),nullable= False)

class Membership(Base):
    __tablename__ = "memberships"
    __table_args__ = (UniqueConstraint('user_id', 'organization_id', name="memberships_user_id_organization_id_key"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    organization_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("organizations.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

class ApiKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(BigInteger,primary_key = True)
    organization_id:Mapped[int] = mapped_column(BigInteger,ForeignKey("organizations.id"),nullable=False)
    name:Mapped[str] = mapped_column(String(255),nullable=False)
    key_prefix:Mapped[str] =mapped_column(String(255),nullable=False)
    key_hash:Mapped[str] = mapped_column(String(255),nullable=False)
    created_at :Mapped[datetime] = mapped_column(DateTime(timezone=True), default = func.now(),nullable=False)
    expires_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True)
    revoked_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True)

class Quota(Base):
    __tablename__ = "quotas"
    __table_args__ = (UniqueConstraint("organization_id",name="quotas_organization_unique"),)

    id:Mapped[int] = mapped_column(BigInteger,primary_key =True)
    organization_id: Mapped[int] = mapped_column(BigInteger,ForeignKey("organizations.id"),nullable=False)
    limitation:Mapped[int] = mapped_column(BigInteger,nullable=False)
    period:Mapped[str] =mapped_column(String(255),nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default= func.now(),nullable=False)
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(),onupdate=func.now(),nullable=False)

class UsageRecord(Base):
    __tablename__ = "usage_records"
    __table_args__ = (UniqueConstraint("api_key_id","usage_date",name="usage_records_api_key_id_usage_date_key"),)

    id:Mapped[int] = mapped_column(BigInteger,primary_key = True)
    api_key_id:Mapped[int] = mapped_column(BigInteger,ForeignKey("api_keys.id"),nullable=False)
    usage_date:Mapped[date] = mapped_column(Date,default = func.current_date(),nullable = False)
    request_count:Mapped[int] = mapped_column(BigInteger,nullable=False)
    created_at:Mapped[datetime] =mapped_column(DateTime(timezone=True),default = func.now(),nullable = False)
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default=func.now(),onupdate=func.now(),nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id:Mapped[int] = mapped_column(BigInteger,primary_key = True)
    user_id:Mapped[int] = mapped_column(BigInteger,ForeignKey("users.id"),nullable=False)
    organization_id:Mapped[int] = mapped_column(BigInteger,ForeignKey("organizations.id"),nullable=False)
    action:Mapped[str] = mapped_column(String(255),nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default = func.now(),nullable=False)
    
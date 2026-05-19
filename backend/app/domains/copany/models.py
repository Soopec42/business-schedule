from sqlalchemy import BigInteger, String, UUID, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum

import uuid
from enum import Enum
from datetime import datetime, timezone

from app.db.session import Base

class CompanyStatus(str, Enum):
    ACTIVE = "ACTIVE" 
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=True)
    phone: Mapped[str] = mapped_column(String(64), nullable=True)
    timezone: Mapped[datetime] = mapped_column(String(64), nullable=False)
    status: Mapped[CompanyStatus] = mapped_column(SQLEnum(CompanyStatus, name = "company_status"), nullable=False, default=CompanyStatus.ACTIVE, server_default=CompanyStatus.ACTIVE.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


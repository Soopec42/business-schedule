from sqlalchemy import BigInteger, String, UUID, ForeignKey, DateTime, func, Boolean
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

class RiskStatus(str, Enum):
    OFF = "OFF"
    LOG_ONLY = "LOG_ONLY"
    WARN_MANAGER = "WARN_MANEGER"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"

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

class CompanySetting(Base):
    __tablename__ = "company_settings"

    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id"), primary_key=True, default=Company.id)
    default_branch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id"), nullable=False)
    default_hold_ttl_minutes: Mapped[int] = mapped_column(BigInteger, default=5, nullable=False)
    min_notice_minutes: Mapped[int] = mapped_column(BigInteger, default=60, nullable=False)
    max_advance_days: Mapped[int] = mapped_column(BigInteger, default=30, nullable=False)
    client_can_cancel: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cancel_before_minutes: Mapped[int] = mapped_column(BigInteger, nullable=True, nullable=False)
    require_phone: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    risk_mode: Mapped[RiskStatus] = mapped_column(SQLEnum(RiskStatus, name = "risk_status"), nullable=False, default=RiskStatus.WARN_MANAGER, server_default=RiskStatus.WARN_MANAGER.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


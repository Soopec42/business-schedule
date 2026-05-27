from sqlalchemy import BigInteger, String, UUID, ForeignKey, DateTime, func, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from typing import Optional
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
    WARN_MANAGER = "WARN_MANAGER"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"

class CompanyBotStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    ERROR = "ERROR"

class BranchStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"

class CompanyMemberRole(str, Enum):
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    SPECIALIST = "SPECIALIST"
    VIEWER = "VIEWER"

class CompanyMemberStatus(str, Enum):
    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REMOVED = "REMOVED"

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    slug: Mapped[str | None] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[CompanyStatus] = mapped_column(SQLEnum(CompanyStatus, name = "company_status"), nullable=False, default=CompanyStatus.ACTIVE, server_default=CompanyStatus.ACTIVE.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())
    specialists: Mapped[list["Specialist"]] = relationship("Specialist", back_populates="company")

class CompanySetting(Base):
    __tablename__ = "company_settings"

    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id"), primary_key=True)
    default_branch_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id"), nullable=True)
    default_hold_ttl_minutes: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    min_notice_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    max_advance_days: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    client_can_cancel: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cancel_before_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    require_phone: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    min_fillable_gap_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=45)
    risk_mode: Mapped[RiskStatus] = mapped_column(SQLEnum(RiskStatus, name = "risk_status"), nullable=False, default=RiskStatus.WARN_MANAGER, server_default=RiskStatus.WARN_MANAGER.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())

class CompanyBot(Base):
    __tablename__ = "company_bots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id"))
    bot_username: Mapped[str] = mapped_column(String(64), nullable=False)
    bot_token_encrypted: Mapped[str] = mapped_column(String(128), nullable=False)
    bot_token_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    webhook_url: Mapped[str] = mapped_column(String(128), nullable=False)
    webhook_secret: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[CompanyBotStatus] = mapped_column(SQLEnum(CompanyBotStatus, name = "company_bot_status"), nullable=False, default=CompanyBotStatus.ACTIVE, server_default=CompanyBotStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())

class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id"))
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    address: Mapped[str | None] = mapped_column(String(256), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str | None] = mapped_column(String(20000), nullable=True)
    status: Mapped[BranchStatus] = mapped_column(SQLEnum(BranchStatus, name="branch_status"), nullable=False, default=BranchStatus.ACTIVE, server_default=BranchStatus.ACTIVE.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())
    
class CompanyMember(Base):
    __tablename__ = "company_member"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    role: Mapped[CompanyMemberRole] = mapped_column(SQLEnum(CompanyMemberRole, name="company_manager_role"), nullable=False, default=CompanyMemberRole.VIEVER.value, server_default=CompanyMemberRole.VIEVER.value)
    status: Mapped[CompanyMemberStatus | None] = mapped_column(SQLEnum(CompanyMemberStatus, name = "company_manager_status"), nullable=True, default=None, server_default=None)
    display_name: Mapped[str] = mapped_column(String(64), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    email: Mapped[EmailStr | None] = mapped_column(String(128), nullable=True)
    telegram_username: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())
    specialist: Mapped[Optional["Specialist"]] = relationship("Specialist", back_populates="member")



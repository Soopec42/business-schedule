from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, DateTime, String, func, UUID
from sqlalchemy import Enum as SQLEnum

from pydantic import EmailStr, field_validator
from datetime import datetime, timezone
from enum import Enum

import uuid

from app.db.session import Base

class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"

class UserRole(str, Enum):
    SYSTEM_OWNER = "SYSTEM_OWNER"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    telegram_username: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    email: Mapped[str | None] = mapped_column(String(128), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[UserStatus] = mapped_column(SQLEnum(UserStatus, name = "user_status"), nullable=False, default=UserStatus.ACTIVE, server_default=UserStatus.ACTIVE.value)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name = "user_role"), nullable=False, default=UserRole.USER, server_default=UserRole.USER)
    password_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    

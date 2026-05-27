from sqlalchemy import String, Integer, BigInteger, UUID, DateTime, ForeignKey, Boolean, func, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum

from typing import Optional
import uuid
from enum import Enum
from datetime import datetime, timezone

from app.db.session import Base

specialist_branches = Table(
    "specialist_branches",
    Base.metadata,
    Column("specialist_id", UUID(as_uuid=True), ForeignKey("specialists.id"), primary_key=True),
    Column("branch_id", UUID(as_uuid=True), ForeignKey("branches.id"), primary_key=True),
)

class SpecialistStatus(str, Enum):
    ACTIVE = "ACTIVE"
    HIDDEN = "HIDDEN"
    ARCHIVED = "ARCHIVED"


class Specialist(Base):
    __tablename__ = "specialists"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    member_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("company_member.id"), nullable=True)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str | None] = mapped_column(String(20000), nullable=True)
    photo_asset_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    photo_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    can_manage_own_slots: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_visible_for_clients: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    status: Mapped[SpecialistStatus] = mapped_column(SQLEnum(SpecialistStatus, name="specialist_status"), nullable=False, default=SpecialistStatus.ACTIVE, server_default=SpecialistStatus.ACTIVE.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())

    company: Mapped["Company"] = relationship("Company", back_populates="specialists")
    member: Mapped[Optional["CompanyMember"]] = relationship("CompanyMember", back_populates="specialists")
    branches: Mapped[list["Branch"]] = relationship(
        "Branch", secondary=specialist_branches, backref="specialists"
    )
    services: Mapped[list["SpecialistService"]] = relationship(
        "SpecialistService", back_populates="specialist"
    )


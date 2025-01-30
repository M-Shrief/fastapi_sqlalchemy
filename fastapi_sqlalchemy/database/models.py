
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Column, DateTime, Enum, ARRAY, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from datetime import datetime
from uuid import UUID

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


class Timestamps:
    """Add created_at and updated_at fields to the table.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column( # Check if onupdate works or not.
        DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP")
    )


role = Enum('Management', 'DBA', 'Analytics', name='role')

class User(Base, Timestamps):
    __tablename__ = "users"

    id: Mapped[UUID] = Column(PG_UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True)
    name: Mapped[str] = Column(String(length=128), nullable=False, unique=True)
    password: Mapped[str] = Column(String(length=128), nullable=False)
    roles = Column(ARRAY(role), nullable=True)




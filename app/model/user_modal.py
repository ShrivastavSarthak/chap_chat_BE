import uuid
from sqlalchemy import Column,String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    isVerifiedEmail = Column(Boolean, default=False)
    role = Column(String, default="user", nullable=False)
    created_at = Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    chats = relationship("Chats", back_populates="user", cascade="all, delete-orphan")
class Guest(Base):
    __tablename__ = "guests"

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    role = Column(String, default="guest", nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
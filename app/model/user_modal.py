import uuid
from sqlalchemy import Column,String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.db import Base
from sqlalchemy.dialects.postgresql import UUID
class User(Base):
    __tablename__ = "Users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, primary_key=True, index=True)
    name = Column(String)
    isVerifiedEmail = Column(Boolean, default=False)
    role = Column(String, default="user", nullable=False)
    created_at = Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )

class Guest(Base):
    __tablename__ = "Guests"

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    role = Column(String, default="guest", nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
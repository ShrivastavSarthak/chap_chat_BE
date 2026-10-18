import uuid
from sqlalchemy import Column,String, Boolean
from app.db.db import Base
from sqlalchemy.dialects.postgresql import UUID
class User(Base):
    __tablename__ = "Users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, primary_key=True, index=True)
    name = Column(String)
    isVerifiedEmail = Column(Boolean, default=False)
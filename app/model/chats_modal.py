import uuid
from app.db.db import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

class Chats(Base):
    __tablename__ = "chats"
    id = Column(UUID(as_uuid=True),primary_key=True,index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    userId = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    isCreated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    user = relationship("User",back_populates="chats")
    history = relationship(
        "ChatHistory",
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by= "ChatHistory.isCreated"
    ) 

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(UUID(as_uuid=True),primary_key=True,index=True, default=uuid.uuid4)
    agentResponse = Column(String, nullable=False)
    userResponse = Column(String, nullable=False)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"))
    isCreated = Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
    )
    chat = relationship("Chats", back_populates="history")
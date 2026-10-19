from sqlalchemy import Column, String, DateTime
from app.db.db import Base

class EmailOTP(Base):
    __tablename__ = "OTP"
    email = Column(String, primary_key=True, index=True)
    otp = Column(String, nullable=False)
    expire_at = Column(DateTime, nullable=False)
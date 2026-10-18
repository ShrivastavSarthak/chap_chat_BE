from pydantic import BaseModel, EmailStr
from uuid import UUID
class UserBase(BaseModel):
    name:str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    name: str | None= None

class UserResponse(UserBase):
    id:UUID
    isVerifiedEmail: bool
    
    class Config:
        from_attributes = True
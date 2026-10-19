from pydantic import BaseModel, EmailStr
class OTPBase(BaseModel):
    email:EmailStr

class OTPMatch(BaseModel):
    email:EmailStr
    otp:str
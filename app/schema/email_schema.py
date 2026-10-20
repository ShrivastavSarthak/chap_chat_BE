from pydantic import BaseModel, EmailStr

class email_schema(BaseModel):
    to:EmailStr
    title: str 
    description:str
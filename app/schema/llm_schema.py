from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_id:str
    user_role:str
    message:str = Field(..., min_length=1, description="User's prompt or question")

class ChatResponse(BaseModel):
    reply:str
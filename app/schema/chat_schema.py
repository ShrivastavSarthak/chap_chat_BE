from pydantic import BaseModel, UUID4


class ChatRequestSchema(BaseModel):
    userId: UUID4
    query:str
    chatId: UUID4

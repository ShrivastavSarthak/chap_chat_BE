from pydantic import BaseModel

class chatResponse(BaseModel):
    userResponse:str
    agentResponse:str
    chat_id:str

class chatHistoryResponse(BaseModel):
    userId:str
    chatId:str
    chatTitle:str
    history:list[chatResponse]= []
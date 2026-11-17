from fastapi import APIRouter,Depends
from app.schema.llm_schema import ChatRequest
from app.schema.chat_schema import ChatRequestSchema
from app.controller.chat_controller import userChatResponse, guestChatResponse, getUsersChat, getChatHistory
from sqlalchemy.orm import Session
from app.db.db import CallDB

bot_route = APIRouter(
    prefix="/chat",
    tags=['Chat API']
)

@bot_route.get("/user/{userId}")
async def fetchUsersChat(userId: str, db:Session = Depends(CallDB)):
    return await getUsersChat(userId, db)

@bot_route.get("/history/{chatId}")
async def fetchUsersChatHistory(chatId: str, db:Session = Depends(CallDB)):
    return await getChatHistory(chatId, db)

@bot_route.post("/guest/response")
async def guestResponse(data:ChatRequest):
    return await guestChatResponse(data)

@bot_route.post('/user/resp')
async def userResponse(data:ChatRequestSchema, db:Session = Depends(CallDB)):
    return await userChatResponse(data,db)
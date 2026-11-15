from  app.schema.chat_schema import ChatRequestSchema
from fastapi.responses import StreamingResponse
from fastapi import HTTPException, status
from app.service.llm_service import LLMResponseService, guestLLMService
from sqlalchemy.orm import Session
from app.model.chats_modal import Chats, ChatHistory
from app.schema.llm_schema import ChatRequest


async def getUsersChat(userId:str,db:Session):
    try:
        findChats = db.query(Chats).filter(Chats.userId == userId).all()
        return {
            "message":"Success",
            "status": status.HTTP_200_OK,
            "data": findChats or [] 
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Internal server error {str(e)}"
        )

async def getChatHistory(chatId:str, db:Session):
    try:
        fetchHistory = db.query(ChatHistory).filter(ChatHistory.chat_id == chatId).all()
        return {
            "message":"Success",
            "status": status.HTTP_200_OK,
            "data": fetchHistory or [] 
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Internal server error {str(e)}"
        )

async def guestChatResponse(payload:ChatRequest):
    try:
        return StreamingResponse(
            guestLLMService(payload.user_id,payload.message),
            media_type="text/plain; charset=utf-8",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response {str(e)}"
        )

async def userChatResponse(payload:ChatRequestSchema, db:Session):
    try:
        dialogue_history=[]
        
        chat_rec = db.query(Chats).filter(Chats.id == payload.chatId).first()
        
        if not chat_rec:
            newChat = Chats(
                id = payload.chatId,
                userId = payload.userId,
                title = payload.query[:10].strip() or "New Chat"
            )
            db.add(newChat)
            db.commit()
        else:
            if chat_rec.userId != payload.userId:
                raise HTTPException(
                    status_code= status.HTTP_403_FORBIDDEN,
                    detail="This chat does not belongs to the this user"
                )
            pastTurn =(
                db.query(ChatHistory).filter(ChatHistory.chat_id == payload.chatId).order_by(ChatHistory.isCreated.asc()).all()
            )
            for turn in pastTurn:
                dialogue_history.append({"role":"user", "content":turn.userResponse})
                dialogue_history.append({"role":"assistant", "content":turn.agentResponse})
        current_history = dialogue_history + [{"role": "user", "content": payload.query}]
        async def stream_and_save():
            full_response = ""
            try:
                async for chunk in LLMResponseService(current_history):
                    full_response += chunk
                    yield chunk
            finally:
                if full_response:
                    new_turn = ChatHistory(
                            chat_id=payload.chatId,
                            userResponse=payload.query,
                            agentResponse=full_response,
                        )
                    db.add(new_turn)
                    db.commit()
        return StreamingResponse(
                    stream_and_save(),
                    media_type="text/plain; charset=utf-8",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "X-Accel-Buffering": "no",
                    }
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error {str(e)}"
        )
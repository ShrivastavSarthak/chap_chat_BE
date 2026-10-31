from app.schema.llm_schema import ChatRequest
from fastapi.responses import StreamingResponse
from app.service.llm_service import llmService
from fastapi import HTTPException,status

async def llmController(payload:ChatRequest):
    try:
        return StreamingResponse(
            llmService(payload.user_id,payload.message),
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
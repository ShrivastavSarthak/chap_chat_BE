from fastapi import APIRouter
from app.controller.llm_controller import llmController
from app.schema.llm_schema import ChatRequest
llm_route = APIRouter(
    prefix="/bot",
    tags=['LLM API']
)

@llm_route.post("/response")
async def llm_response(query:ChatRequest):
    return await llmController(query)
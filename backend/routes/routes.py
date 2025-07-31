from fastapi import APIRouter, Request
from pydantic import BaseModel
from agents.chat_agent import get_chat_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = get_chat_response(request.message)
    return {"response": response}

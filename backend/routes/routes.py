from fastapi import APIRouter
from pydantic import BaseModel
from agents.chat_agent import get_chat_response
import logging

# Logging setup for this module
logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/v1/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Incoming message: {request.message}")
    
    try:
        response = get_chat_response(request.message)
        logger.info(f"Response from agent: {response}")
        return {"response": response}
    
    except Exception as e:
        logger.error(f"Error while processing message: {e}")
        return {"error": "Internal server error"}

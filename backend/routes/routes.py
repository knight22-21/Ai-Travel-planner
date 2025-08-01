from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agents.chat_agent import get_chat_response
from pdf_utils.pdf_generator import generate_pdf_from_chat
import logging

# Logging setup for this module
logger = logging.getLogger(__name__)

router = APIRouter()

# Request models
class ChatRequest(BaseModel):
    message: str

class ChatHistoryRequest(BaseModel):
    history: list

# Chat endpoint
@router.post("/v1/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Incoming message: {request.message}")
    
    try:
        response = get_chat_response(request.message)
        logger.info(f"Response from agent: {response}")
        return {"response": response}
    
    except Exception as e:
        logger.error(f"Error while processing message: {e}", exc_info=True)
        return {"error": "Internal server error"}

# PDF generation endpoint
@router.post("/v1/pdf")
async def download_pdf(chat_data: ChatHistoryRequest):
    logger.info("Received request to generate PDF from chat history.")
    try:
        pdf_buffer = generate_pdf_from_chat(chat_data.history)
        logger.info("PDF generated successfully.")
        return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=chat_history.pdf"
        })
    except Exception as e:
        logger.error(f"Failed to generate PDF: {e}", exc_info=True)
        return {"error": "Failed to generate PDF"}

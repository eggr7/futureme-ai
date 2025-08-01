from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.logic import get_response
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str = "success"
    error: str = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    Chat endpoint that handles user messages and returns AI responses.
    Supports both LLM and static response modes with comprehensive error handling.
    """
    try:
        # Validate input
        if not chat_message.message or not chat_message.message.strip():
            raise HTTPException(
                status_code=400, 
                detail="Message cannot be empty"
            )
        
        # Log the incoming message (without sensitive data)
        logger.info(f"Processing chat message: {chat_message.message[:50]}...")
        
        # Generate response using the enhanced logic
        ai_response = get_response(chat_message.message.strip())
        
        # Validate response
        if not ai_response:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate response"
            )
        
        logger.info("Successfully generated response")
        
        return ChatResponse(
            response=ai_response,
            status="success"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
        
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error in chat endpoint: {str(e)}")
        
        # Return a user-friendly error response
        return ChatResponse(
            response="I'm sorry, I'm having trouble processing your request right now. Please try again in a moment.",
            status="error",
            error="Internal server error"
        )
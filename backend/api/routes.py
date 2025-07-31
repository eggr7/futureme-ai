from fastapi import APIRouter
from pydantic import BaseModel
from core.logic import get_response

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    Chat endpoint that receives user messages and returns AI responses
    """
    response = get_response(chat_message.message)
    return ChatResponse(reply=response)
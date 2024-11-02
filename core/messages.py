from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from core.constants import (
    ROLE_SYSTEM, ROLE_USER, ROLE_ASSISTANT, ROLE_TOOL
)

class Function(BaseModel):
    name: str
    arguments: str

class ToolCall(BaseModel):
    id: str
    type: str = "function"
    function: Function

class Message(BaseModel):
    role: str
    content: Optional[str] = None
    name: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None

# API Request/Response models
class ChatRequest(BaseModel):
    messages: List[Message]
    conversation_id: Optional[str] = None
    thread_id: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    result: str
    conversation_id: Optional[str]
    thread_id: Optional[str]
    session_id: Optional[str]
    thread_status: str
    messages: List[Message]
    error_details: Optional[str] = None
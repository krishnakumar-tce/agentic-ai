from typing import Dict, Any, List, Optional
import logging
from services.openai_service import OpenAIClient
from core.messages import Message
from .constants import (
    STATUS_SUCCESS, STATUS_ERROR,
    THREAD_ACTIVE, THREAD_COMPLETE, THREAD_ERROR,
    ROLE_ASSISTANT, ROLE_TOOL
)
import json

logger = logging.getLogger(__name__)

class Application:
    """Core application class that orchestrates the agent system"""
    
    def __init__(self, triage_agent):
        self.client = OpenAIClient()
        self.triage_agent = triage_agent
    
    async def process_request(
        self,
        messages: List[Dict[str, Any]],
        conversation_id: Optional[str] = None,
        thread_id: Optional[str] = None,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a chat request through the agent system"""
        try:
            logger.info(f"Processing request for conversation: {conversation_id}, thread: {thread_id}")
            
            # Process through triage agent
            current_messages, had_error, is_server_error = await self.triage_agent.process_message(messages, self.client)
            
            # Get the last assistant message for the response
            last_assistant_message = None
            for msg in reversed(current_messages):
                if msg["role"] == ROLE_ASSISTANT:
                    last_assistant_message = msg
                    break
            
            # Determine thread status and result
            thread_status = THREAD_ACTIVE
            result = ""
            
            if had_error:
                if is_server_error:
                    thread_status = THREAD_ERROR
                # else keep THREAD_ACTIVE for client errors (400)
                result = last_assistant_message.get("content", "An error occurred") if last_assistant_message else "An error occurred"
            elif last_assistant_message:
                # Get the result content
                result = last_assistant_message.get("content", "")
                
                # Check if this was a specialized agent execution
                was_specialized_agent = False
                for msg in current_messages:
                    if msg.get("tool_calls"):
                        was_specialized_agent = True
                        break
                
                if was_specialized_agent:
                    # If it was a specialized agent, complete only if tool was executed successfully
                    tool_executed = any(
                        msg["role"] == ROLE_TOOL and not json.loads(msg["content"]).get("error")
                        for msg in current_messages
                    )
                    if tool_executed:
                        thread_status = THREAD_COMPLETE
                else:
                    # For triage agent, keep thread active if asking questions
                    thread_status = THREAD_ACTIVE
            
            response = {
                "result": result or "",  # Ensure result is never None
                "conversation_id": conversation_id,
                "thread_id": thread_id,
                "session_id": session_id,
                "thread_status": thread_status,
                "messages": current_messages,
                "error_details": str(last_assistant_message.get("error")) if had_error else None
            }
            
            # Safe string slicing for logging
            log_result = result[:100] + "..." if result else ""
            logger.info(f"Request processed. Status: {thread_status}, Result: {log_result}")
            return response
            
        except Exception as e:
            logger.exception("Error processing request")
            return {
                "result": STATUS_ERROR,
                "conversation_id": conversation_id,
                "thread_id": thread_id,
                "session_id": session_id,
                "thread_status": THREAD_ERROR,
                "messages": messages,
                "error_details": str(e)
            }
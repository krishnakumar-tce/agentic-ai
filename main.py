import logging
from typing import Dict, Any, List, Optional
from services.openai_service import OpenAIClient
from core.factory import AgentFactory
from core.messages import Message
from core.constants import (
    STATUS_SUCCESS, STATUS_ERROR,
    THREAD_ACTIVE, THREAD_COMPLETE, THREAD_ERROR,
    ROLE_ASSISTANT, ROLE_TOOL
)
import json

logger = logging.getLogger(__name__)

class AgenticAIApplication:
    """Main application class that orchestrates the agent system"""
    
    def __init__(self, factory: AgentFactory = None):
        self.factory = factory or AgentFactory()
        self.client = OpenAIClient()
        
        # Initialize agents from registry
        self.agents = {}
        for agent_name in self.factory.agent_registry.available_agents:
            self.agents[agent_name] = self.factory.get_agent(agent_name)
            
        # Ensure we have a triage agent
        if 'agent_triage' not in self.agents:
            raise ValueError("Triage agent must be defined in configuration")
            
        logger.info(f"Initialized AgenticAI with agents: {list(self.agents.keys())}")
    
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
            
            # Convert messages to Message objects
            message_objects = [
                msg if isinstance(msg, Message) else Message(**msg)
                for msg in messages
            ]
            
            # Process through triage agent first
            current_messages, had_error, is_server_error = await self.agents['agent_triage'].process_message(
                message_objects, 
                self.client
            )
            
            # Check for routing in the last tool response
            routing = None
            for msg in reversed(current_messages):
                if msg.role == ROLE_TOOL:
                    try:
                        tool_result = json.loads(msg.content)
                        if isinstance(tool_result, dict):
                            routing = tool_result.get("routing")
                            if routing:
                                break
                    except (json.JSONDecodeError, AttributeError):
                        logger.warning(f"Invalid tool response: {msg.content}")
                        continue
            
            # Route to appropriate agent if routing exists
            if routing:
                if routing == "transfer_to_unsupported":
                    # Special case: unsupported request
                    return {
                        "result": "I apologize, but I cannot help with that request.",
                        "conversation_id": conversation_id,
                        "thread_id": thread_id,
                        "session_id": session_id,
                        "thread_status": THREAD_COMPLETE,  # Mark as complete
                        "messages": current_messages,
                        "error_details": None
                    }
                    
                # Normal routing continues...
                target_agent = routing.replace("transfer_to_", "")
                if target_agent in self.agents:
                    logger.info(f"Routing to: {target_agent}")
                    current_messages, had_error, is_server_error = await self.agents[target_agent].process_message(
                        message_objects,
                        self.client
                    )
                else:
                    logger.error(f"Unknown routing target: {target_agent}")
                    had_error = True
                    is_server_error = True
            
            # Get the last assistant message for the response
            last_assistant_message = None
            for msg in reversed(current_messages):
                if msg.role == ROLE_ASSISTANT:
                    last_assistant_message = msg
                    break
            
            # Determine thread status and result
            thread_status = THREAD_ACTIVE
            result = ""
            
            if had_error:
                if is_server_error:
                    thread_status = THREAD_ERROR
                result = last_assistant_message.content if last_assistant_message else "An error occurred"
            elif last_assistant_message:
                result = last_assistant_message.content or ""
                
                # Check if this was a specialized agent execution
                was_specialized_agent = False
                for msg in current_messages:
                    if msg.tool_calls:
                        was_specialized_agent = True
                        break
                
                if was_specialized_agent:
                    tool_executed = any(
                        msg.role == ROLE_TOOL and not json.loads(msg.content).get("error")
                        for msg in current_messages
                    )
                    if tool_executed:
                        thread_status = THREAD_COMPLETE
                else:
                    thread_status = THREAD_ACTIVE
            
            return {
                "result": result,
                "conversation_id": conversation_id,
                "thread_id": thread_id,
                "session_id": session_id,
                "thread_status": thread_status,
                "messages": current_messages,
                "error_details": str(last_assistant_message.error) if had_error else None
            }
            
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
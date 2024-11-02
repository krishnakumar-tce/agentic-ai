from typing import List, Dict, Any, Tuple
from pydantic import BaseModel
from .messages import Message
import json
import logging
import asyncio
from .constants import (
    ROLE_SYSTEM, ROLE_USER, ROLE_ASSISTANT, ROLE_TOOL
)
from utils.logger import log_openai_exchange, log_openai_response

logger = logging.getLogger(__name__)

class Agent(BaseModel):
    """Model for agent configuration"""
    name: str
    instructions: str
    functions: List[Dict[str, Any]]

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str, instructions: str = None, tools: List[Any] = None):
        self.name = name
        self.instructions = instructions
        self.functions = tools or []
        self._agent = None
    
    def _initialize_agent(self):
        """Initialize the Agent model once we have all configuration"""
        if self._agent is None and self.instructions:  # Only create if we have instructions
            # Convert tool objects to their definitions
            function_definitions = [
                tool.get_tool_definition() for tool in self.functions
            ] if self.functions else []
            
            self._agent = Agent(
                name=self.name,
                instructions=self.instructions,
                functions=function_definitions
            )
    
    @property
    def tools(self):
        """Return tools in OpenAI format"""
        self._initialize_agent()  # Ensure agent is initialized
        return self._agent.functions if self._agent else []

    async def process_message(self, messages: List[Message], client) -> Tuple[List[Message], bool, bool]:
        """Process a message and handle any tool calls"""
        logger.info(f"=== {self.name} processing message ===")
        
        # Ensure agent is initialized
        self._initialize_agent()
        if not self._agent:
            raise ValueError(f"Agent {self.name} not properly configured - missing instructions")
        
        # Add system message
        current_messages = [
            Message(
                role=ROLE_SYSTEM,
                content=self.instructions
            )
        ] + messages
        
        # Log OpenAI exchange
        log_openai_exchange(logger, self.name, current_messages, self.tools)
        
        # Get response from OpenAI
        completion = await client.chat(
            messages=current_messages,
            tools=self.tools
        )
        
        assistant_message = Message(**completion.choices[0].message.model_dump())
        log_openai_response(logger, self.name, assistant_message)
        
        # Handle tool calls if any
        if assistant_message.tool_calls:
            return await self._handle_tool_calls(assistant_message, current_messages, client)
        
        # No tool calls, just return the conversation
        current_messages.append(assistant_message)
        return current_messages[1:], False, False

    async def _handle_tool_calls(self, assistant_message, current_messages, client) -> Tuple[List[Message], bool, bool]:
        """Handle tool calls from OpenAI"""
        current_messages.append(assistant_message)
        
        # Execute all tool calls in parallel
        tool_results = await asyncio.gather(*[
            self.execute_tool(
                tool_call.function.name,
                **json.loads(tool_call.function.arguments)
            )
            for tool_call in assistant_message.tool_calls
        ], return_exceptions=True)
        
        # Add tool responses
        for tool_call, result in zip(assistant_message.tool_calls, tool_results):
            if isinstance(result, Exception):
                error_content = {
                    "error": str(result),
                    "type": result.__class__.__name__
                }
                content = json.dumps(error_content)
            else:
                content = json.dumps(result)
                
            tool_response = Message(
                role=ROLE_TOOL,
                tool_call_id=tool_call.id,
                name=tool_call.function.name,
                content=content
            )
            current_messages.append(tool_response)
        
        # Get final response
        completion = await client.chat(
            messages=current_messages,
            tools=self.tools
        )
        next_message = Message(**completion.choices[0].message.model_dump())
        
        # Check if OpenAI wants to make more tool calls
        if next_message.tool_calls:
            # Recursively handle the new tool calls
            return await self._handle_tool_calls(next_message, current_messages, client)
            
        # No more tool calls, add final message and return
        current_messages.append(next_message)
        return current_messages[1:], False, False

    async def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool - now handled directly in base class"""
        logger.info("\n" + "▲" * 50)  # Added triangles
        logger.info(f"{self.name} executing {tool_name}")
        logger.info("▲" * 50)  # Added triangles
        
        for tool in self.functions:
            if tool.name == tool_name:
                return await tool.execute(**kwargs)
                
        raise ValueError(f"Unknown tool: {tool_name}")
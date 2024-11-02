from openai import AsyncOpenAI
from core.messages import Message
from core.settings import get_settings
from typing import List, Dict, Any, Optional
import logging
import json

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        self.settings = get_settings()
        self.openai = AsyncOpenAI(
            api_key=self.settings.OPENAI_API_KEY,
            organization=self.settings.OPENAI_ORG_ID if hasattr(self.settings, 'OPENAI_ORG_ID') else None
        )
    
    async def chat(self, messages: List[Message], tools: Optional[List[Dict[str, Any]]] = None):
        """Simple OpenAI chat completion"""
        try:
            messages_dict = [
                message.model_dump() if isinstance(message, Message)
                else Message(**message).model_dump()
                for message in messages
            ]
            
            # Only log tool calls from response
            response = await self.openai.chat.completions.create(
                model=self.settings.OPENAI_MODEL,
                messages=messages_dict,
                tools=tools,
                tool_choice="auto" if tools else None
            )
            
            if response.choices[0].message.tool_calls:
                tool_calls = [t.function.name for t in response.choices[0].message.tool_calls]
                logger.debug(f"OpenAI tool calls: {tool_calls}")
            
            return response
            
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            raise
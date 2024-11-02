from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseTool:
    """Base class for all tools"""
    
    def __init__(self, name: str, description: str, schema: Dict[str, Any]):
        self.name = name
        self.description = description
        self.schema = schema
        logger.debug(f"Initialized tool: {name}")
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition in OpenAI format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.schema,
                "strict": True
            }
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement execute")
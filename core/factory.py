from typing import Dict, Any, Optional
import logging
from core.registry import Registry, AgentRegistry, ToolRegistry
from core.base_agent import BaseAgent
from core.base_tool import BaseTool

logger = logging.getLogger(__name__)

class AgentFactory:
    """Factory for creating agent instances"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.agent_registry = AgentRegistry()
            cls._instance.tool_registry = ToolRegistry()
            logger.debug("Initialized AgentFactory")
        return cls._instance
    
    def get_agent(self, agent_type: str) -> Any:
        """Get an agent instance by type"""
        logger.info(f"Creating agent: {agent_type}")
        return self.agent_registry.get_agent(agent_type)
    
    def get_tool(self, tool_name: str) -> Any:
        """Get a tool instance by name"""
        logger.info(f"Creating tool: {tool_name}")
        return self.tool_registry.get_tool(tool_name)
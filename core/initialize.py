from core.registry import Registry
from core.base_tool import BaseTool
from core.base_agent import BaseAgent
from core.factory import AgentFactory
from utils.yaml_loader import load_yaml_config
from pathlib import Path
import logging
import importlib

logger = logging.getLogger(__name__)

def get_class(class_path: str):
    """Dynamically import and return a class"""
    try:
        # Remove any agentic_ai prefix
        if class_path.startswith('agentic_ai.'):
            class_path = class_path[len('agentic_ai.'):]
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except Exception as e:
        logger.error(f"Error importing class {class_path}: {e}")
        raise

def initialize_application():
    """Initialize all registries and components from YAML configs"""
    logger.info("Initializing application components")
    
    # Get config directory
    config_dir = Path(__file__).parent.parent / 'config'
    
    # Initialize factory
    factory = AgentFactory()
    
    # Load tool configurations
    tools_config = load_yaml_config(config_dir / 'tools.yaml')
    for tool_name, tool_info in tools_config['tools'].items():
        # For inner tools, use BaseTool class
        if tool_name.startswith('tool_'):
            tool_class = get_class('core.base_tool.BaseTool')
        else:
            # For triage tools, get class from config
            tool_class = get_class(tool_info['class'])
            
        factory.tool_registry.register(
            tool_name,
            tool_class,
            **tool_info
        )
    logger.info(f"Registered tools: {factory.tool_registry.available_tools}")
    
    # Load agent configurations
    agents_config = load_yaml_config(config_dir / 'agents.yaml')
    for agent_name, agent_info in agents_config['agents'].items():
        config = {k: v for k, v in agent_info.items() if k not in ['class', 'name']}
        from core.base_agent import BaseAgent
        factory.agent_registry.register(
            agent_name,
            BaseAgent,
            **config
        )
    logger.info(f"Registered agents: {factory.agent_registry.available_agents}")
    
    return factory

# Add __all__ to explicitly state what can be imported
__all__ = ['initialize_application', 'get_class']
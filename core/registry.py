from typing import Dict, Type, Any
import logging
import importlib
from pathlib import Path

logger = logging.getLogger(__name__)

def to_pascal_case(snake_str: str) -> str:
    """Convert tool_product_finder to ProductFinder"""
    # Remove tool_ prefix
    if snake_str.startswith('tool_'):
        snake_str = snake_str[5:]
    # Split by underscore and capitalize each part
    return ''.join(part.title() for part in snake_str.split('_'))

class Registry:
    """Base registry for components"""
    _instance = None
    _registry_type = "component"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._items = {}
            cls._instance._configs = {}
        return cls._instance
    
    def register(self, name: str, item_class: Type, **kwargs):
        """Register a component with its configuration"""
        logger.info(f"Registering {self._registry_type}: {name}")
        self._items[name] = {
            'class': item_class,
            'config': kwargs
        }
    
    def get(self, name: str) -> Any:
        """Get an instance of a registered component"""
        if name not in self._items:
            raise ValueError(f"{self._registry_type} not registered: {name}")
            
        item_info = self._items[name]
        cls = item_info['class']
        config = item_info['config']
        
        # Handle triage tools
        if name.startswith('transfer_to_'):
            if cls.__name__ == 'TriageTool':
                return cls(name=name, description=config['description'])
            else:
                raise ValueError(f"Invalid class for transfer tool: {cls.__name__}")
        
        # Handle inner tools
        if name.startswith('tool_'):
            try:
                # Convert tool name to class names
                pascal_name = to_pascal_case(name)
                
                # Import the tool's module
                module = importlib.import_module(f"extensions.{name}")
                
                try:
                    # Get components using naming convention
                    service_class = getattr(module, f"{pascal_name}Service")
                    schema = getattr(module, f"{pascal_name}Schema")
                except AttributeError as e:
                    logger.error(f"""Failed to find required component for tool {name}:
                        Looking for:
                        - Service class: {pascal_name}Service
                        - Schema constant: {pascal_name}Schema
                        Error: {str(e)}
                    """)
                    raise
                
                # Create tool instance
                tool = cls(
                    name=name,
                    description=config['description'],
                    schema=schema
                )
                
                # Add service
                tool.service = service_class()
                
                # Add execute method
                async def execute(**kwargs):
                    try:
                        # No Request class validation, pass kwargs directly
                        return await tool.service.execute(kwargs)
                    except Exception as e:
                        logger.error(f"Error executing {name}: {str(e)}")
                        raise
                        
                tool.execute = execute
                return tool
                
            except ImportError as e:
                logger.error(f"Failed to import tool module {name}: {e}")
                raise
            except Exception as e:
                logger.error(f"Error creating tool {name}: {e}")
                raise
        
        # For BaseAgent
        if cls.__name__ == 'BaseAgent':
            instance = cls(name=name)
            self._configure_instance(instance, config)
            return instance
        
        # Default case - shouldn't reach here
        raise ValueError(f"Unknown component type: {cls.__name__}")
    
    def _configure_instance(self, instance: Any, config: Dict[str, Any]):
        """Configure instance with remaining parameters"""
        for key, value in config.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
    
    @property
    def available_items(self) -> list[str]:
        """Get list of registered components"""
        return list(self._items.keys())

class AgentRegistry(Registry):
    """Registry for agents"""
    _registry_type = "agent"
    
    @property
    def available_agents(self) -> list[str]:
        return self.available_items
    
    def get_agent(self, name: str) -> Any:
        """Alias for get() to make code more readable"""
        return self.get(name)
    
    def _configure_instance(self, instance: Any, config: Dict[str, Any]):
        """Configure agent with instructions and tools"""
        if 'instructions' in config:
            instance.instructions = config['instructions']
        
        if 'tools' in config:
            tool_registry = ToolRegistry()
            instance.functions = [
                tool_registry.get_tool(tool_name) 
                for tool_name in config['tools']
            ]

class ToolRegistry(Registry):
    """Registry for tools"""
    _registry_type = "tool"
    
    def _configure_instance(self, instance: Any, config: Dict[str, Any]):
        """Configure tool with its parameters"""
        for key, value in config.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
    
    @property
    def available_tools(self) -> list[str]:
        return self.available_items
    
    def get_tool(self, name: str) -> Any:
        """Alias for get() to make code more readable"""
        return self.get(name)

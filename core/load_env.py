from dotenv import load_dotenv
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_environment():
    """Load environment variables from all .env files"""
    # Get project root directory
    root_dir = Path(__file__).parent.parent
    
    # First load tool-specific .env files from extensions
    extensions_dir = root_dir / 'extensions'
    for tool_dir in extensions_dir.glob('tool_*'):
        env_path = tool_dir / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            logger.debug(f"Loaded environment from {env_path}")
    
    # Then load the main .env file (for OpenAI credentials)
    root_env_path = root_dir / '.env'
    if not root_env_path.exists():
        raise ValueError(f"Missing main .env file at {root_env_path}")
    load_dotenv(root_env_path)
    
    # Verify OpenAI environment variables
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("Missing OPENAI_API_KEY in root .env file")
    if not os.getenv('OPENAI_MODEL'):
        raise ValueError("Missing OPENAI_MODEL in root .env file")

import logging
from .core.initialize import initialize_application

# Configure root logger
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(message)s'
)

# Set specific loggers to appropriate levels
logging.getLogger('agentic_ai').setLevel(logging.INFO)

# Silence everything except our narrative logs
noisy_loggers = [
    'agentic_ai.tools',
    'httpx',
    'httpcore',
    'asyncio',
    'aiohttp',
    'uvicorn',
    'uvicorn.error',
    'fastapi'
]
for logger_name in noisy_loggers:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

# Initialize application components and get factory
factory = initialize_application()

# Export factory for use by other modules
__all__ = ['factory']

# Empty file to make the directory a Python package 
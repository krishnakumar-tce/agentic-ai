import logging
from typing import Any, Dict, List, Optional
import json
from core.messages import Message

def get_logger(name: str) -> logging.Logger:
    """Get a logger with standard formatting"""
    return setup_logger(name)

def setup_logger(name: str) -> logging.Logger:
    """Configure a logger with standard formatting"""
    logger = logging.getLogger(name)
    return logger

def log_conversation_start(logger: logging.Logger, conversation_id: str, thread_id: str):
    """Log the start of a conversation"""
    logger.info("\n" + "=" * 80)
    logger.info(f"Starting new conversation: {conversation_id} (Thread: {thread_id})")
    logger.info("=" * 80)

def log_agent_handoff(logger: logging.Logger, from_agent: str, to_agent: str, context: str):
    """Log agent handoffs"""
    logger.info("\n" + "-" * 60)
    logger.info(f"🔄 {from_agent} transferring control to {to_agent}")
    logger.info(f"Context: {context}")
    logger.info("-" * 60)

def log_openai_exchange(logger: logging.Logger, agent_name: str, messages: List[Message], tools: Optional[List[Dict]] = None):
    """Log OpenAI exchange details"""
    logger.info(f"\n=== {agent_name} OpenAI Exchange ===")
    
    # Log messages
    for msg in messages:
        if msg.role == "user":
            logger.info(f"User: {msg.content}")
        elif msg.role == "assistant":
            logger.info(f"Assistant: {msg.content}")
            if msg.tool_calls:
                logger.info(f"Tool Calls: {msg.tool_calls}")
        elif msg.role == "system":
            logger.info(f"System: {msg.content}")
    
    # Log tools if any
    if tools:
        logger.info(f"Available Tools: {[t['function']['name'] for t in tools]}")

def log_openai_response(logger: logging.Logger, agent_name: str, message: Message):
    """Log OpenAI's response in a narrative format"""
    logger.info("\n" + "▲" * 50)
    logger.info(f"🤖 OpenAI's response to {agent_name}:")
    
    if message.content:
        logger.info(f"Content: {message.content}")
    
    if message.tool_calls:
        tool_name = message.tool_calls[0].function.name
        logger.info(f"Requested tool: {tool_name}")
    
    logger.info("▲" * 50)
def log_tool_execution(logger: logging.Logger, tool_name: str):
    """Log just the tool being executed"""
    logger.info(f"🔧 Executing: {tool_name}")

def log_error(logger: logging.Logger, error: Exception, context: str = None):
    """Log errors with context"""
    logger.error("\n" + "!" * 50)
    logger.error("❌ Error occurred" + (f" during {context}" if context else ""))
    logger.error(f"Type: {type(error).__name__}")
    logger.error(f"Message: {str(error)}")
    logger.error("!" * 50)

def log_conversation_end(logger: logging.Logger, conversation_id: str, status: str):
    """Log the end of a conversation"""
    logger.info("\n" + "=" * 80)
    logger.info(f"Ending conversation {conversation_id} with status: {status}")
    logger.info("=" * 80)

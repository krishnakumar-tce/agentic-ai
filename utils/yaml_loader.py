import yaml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_yaml_config(file_path: str) -> dict:
    """Load YAML configuration file"""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading YAML file {file_path}: {e}")
        raise 
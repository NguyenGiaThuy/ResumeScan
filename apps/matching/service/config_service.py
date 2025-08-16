"""
Configuration Service
Handles loading and managing application configurations
"""
import os
import json
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from file."""
    config_path = os.environ.get("CONFIG_FILE", "/app/configs/ai-elevate-dev.json")
    configs = {}
    if config_path and os.path.isfile(config_path):
        with open(config_path, "r") as f:
            configs = json.load(f)
    return configs


def get_embedding_config() -> Dict[str, str]:
    """Get embedding configuration."""
    configs = load_config()
    return {
        "region_name": configs["aws"]["bedrock"]["model_region"],
        "model_id": configs["aws"]["bedrock"]["embedding_model_id"],
    }


def get_model_config() -> Dict[str, Any]:
    """Get model configuration."""
    configs = load_config()
    return {
        "model_id": configs["aws"]["bedrock"]["model_id"],
        "region": configs["aws"]["bedrock"]["model_region"],
        "model_kwargs": configs["aws"]["bedrock"]["model_kwargs"],
    }

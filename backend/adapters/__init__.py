"""
AI Model Adapters

Unified interface for all AI model providers.
Each adapter implements the BaseAdapter interface.
"""

from .base import BaseAdapter
from .openai import OpenAIAdapter
from .anthropic import AnthropicAdapter
from .google import GoogleAdapter
from .xai import XAIAdapter

__all__ = [
    "BaseAdapter",
    "OpenAIAdapter",
    "AnthropicAdapter",
    "GoogleAdapter",
    "XAIAdapter",
]

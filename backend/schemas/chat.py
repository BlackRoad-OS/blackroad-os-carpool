"""
Chat Schemas

Request/Response models for chat endpoints.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class ChatMessage(BaseModel):
    """Single chat message"""
    role: str
    content: str
    model_used: Optional[str] = None
    created_at: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request from user"""
    workspace_id: str
    conversation_id: Optional[str] = None
    message: str
    preferred_model: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response to user"""
    conversation_id: str
    message: ChatMessage
    model_used: str
    tokens_used: int
    roadcoin_cost: float
    routing_decision: Dict[str, Any]

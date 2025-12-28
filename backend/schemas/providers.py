"""
Provider Schemas

API key management.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProviderConfig(BaseModel):
    """Add API key request"""
    provider: str  # openai, anthropic, google, xai
    api_key: str
    endpoint_url: Optional[str] = None


class ProviderResponse(BaseModel):
    """Provider response"""
    provider: str
    key_hint: str
    is_valid: bool
    last_tested_at: Optional[datetime] = None
    created_at: datetime

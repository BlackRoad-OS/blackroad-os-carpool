"""
Workspace Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class WorkspaceCreate(BaseModel):
    """Create workspace request"""
    name: str
    settings: Optional[Dict[str, Any]] = {}


class WorkspaceResponse(BaseModel):
    """Workspace response"""
    id: str
    name: str
    slug: str
    plan: str
    created_at: datetime
    updated_at: datetime

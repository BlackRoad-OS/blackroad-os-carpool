"""
CarPool by BlackRoad OS, Inc.
Multi-AI Orchestration Platform

Main FastAPI application entry point.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import uuid
from datetime import datetime

from lucidia import lucidia, ModelProvider, RoutingDecision
from adapters import OpenAIAdapter, AnthropicAdapter, GoogleAdapter, XAIAdapter

# Initialize FastAPI app
app = FastAPI(
    title="CarPool API",
    description="Multi-AI orchestration platform by BlackRoad OS, Inc.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://app.blackroad.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory provider registry  { workspace_id -> { provider_name -> api_key } }
# A persistent implementation would store these encrypted in the database.
# ---------------------------------------------------------------------------
_workspace_providers: Dict[str, Dict[str, str]] = {}


def _get_available_providers(workspace_id: str) -> List[ModelProvider]:
    """Return the list of providers that have a key for this workspace."""
    ws = _workspace_providers.get(workspace_id, {})
    available = []
    if ws.get("openai") or os.environ.get("OPENAI_API_KEY"):
        available.append(ModelProvider.OPENAI)
    if ws.get("anthropic") or os.environ.get("ANTHROPIC_API_KEY"):
        available.append(ModelProvider.ANTHROPIC)
    if ws.get("google") or os.environ.get("GOOGLE_API_KEY"):
        available.append(ModelProvider.GOOGLE)
    if ws.get("xai") or os.environ.get("XAI_API_KEY"):
        available.append(ModelProvider.XAI)
    return available


def _build_adapter(provider: ModelProvider, workspace_id: str):
    """Instantiate the adapter for the given provider using the workspace key."""
    ws = _workspace_providers.get(workspace_id, {})

    if provider == ModelProvider.OPENAI:
        key = ws.get("openai") or os.environ.get("OPENAI_API_KEY", "")
        return OpenAIAdapter(api_key=key) if key else None

    if provider == ModelProvider.ANTHROPIC:
        key = ws.get("anthropic") or os.environ.get("ANTHROPIC_API_KEY", "")
        return AnthropicAdapter(api_key=key) if key else None

    if provider == ModelProvider.GOOGLE:
        key = ws.get("google") or os.environ.get("GOOGLE_API_KEY", "")
        return GoogleAdapter(api_key=key) if key else None

    if provider == ModelProvider.XAI:
        key = ws.get("xai") or os.environ.get("XAI_API_KEY", "")
        return XAIAdapter(api_key=key) if key else None

    return None


# Request/Response Models
class ChatMessage(BaseModel):
    role: str
    content: str
    model_used: Optional[str] = None
    created_at: Optional[datetime] = None

class ChatRequest(BaseModel):
    workspace_id: str
    conversation_id: Optional[str] = None
    message: str
    preferred_model: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str
    message: ChatMessage
    model_used: str
    tokens_used: int
    routing_decision: Dict[str, Any]

class ProviderConfig(BaseModel):
    provider: str  # openai, anthropic, google, xai
    api_key: str
    enabled: bool = True

class WorkspaceCreate(BaseModel):
    name: str
    settings: Optional[Dict[str, Any]] = {}

# Health check
@app.get("/")
async def root():
    return {
        "service": "CarPool API",
        "version": "0.1.0",
        "status": "operational",
        "company": "BlackRoad OS, Inc.",
        "tagline": "Bring any AI. Train your own. Never leave."
    }

@app.get("/health")
async def health_check():
    providers_configured = bool(
        os.environ.get("OPENAI_API_KEY")
        or os.environ.get("ANTHROPIC_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("XAI_API_KEY")
        or any(_workspace_providers.values())
    )
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "operational",
            "lucidia": "operational",
            "database": "not_configured",
            "redis": "not_configured",
            "providers_configured": providers_configured
        }
    }

# Workspace Management
@app.post("/api/v1/workspaces")
async def create_workspace(workspace: WorkspaceCreate):
    """Create a new workspace for a user"""
    # TODO: Implement database storage
    return {
        "id": "ws_temp_001",
        "name": workspace.name,
        "created_at": datetime.utcnow().isoformat(),
        "settings": workspace.settings
    }

@app.get("/api/v1/workspaces/{workspace_id}")
async def get_workspace(workspace_id: str):
    """Get workspace details"""
    # TODO: Implement database lookup
    return {
        "id": workspace_id,
        "name": "Default Workspace",
        "created_at": datetime.utcnow().isoformat()
    }

# API Key Management
@app.post("/api/v1/workspaces/{workspace_id}/providers")
async def add_provider(workspace_id: str, config: ProviderConfig):
    """Add AI provider API key to workspace"""
    if workspace_id not in _workspace_providers:
        _workspace_providers[workspace_id] = {}
    _workspace_providers[workspace_id][config.provider] = config.api_key
    return {
        "workspace_id": workspace_id,
        "provider": config.provider,
        "status": "configured",
        "added_at": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/workspaces/{workspace_id}/providers")
async def list_providers(workspace_id: str):
    """List configured AI providers for workspace"""
    ws = _workspace_providers.get(workspace_id, {})
    configured = [{"provider": k, "status": "configured"} for k in ws]
    # Surface env-var providers that aren't already listed
    env_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
        "xai": "XAI_API_KEY",
    }
    for provider, env_var in env_map.items():
        if os.environ.get(env_var) and provider not in ws:
            configured.append({"provider": provider, "status": "configured_via_env"})
    return {"workspace_id": workspace_id, "providers": configured}

# Chat / Orchestration
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint — routes to Lucidia for AI orchestration.

    1. Lucidia analyzes the task
    2. Selects optimal model from the workspace's configured providers
    3. Executes request via the matching adapter
    4. Returns response with routing metadata
    """
    # 1. Determine available providers
    available_providers = _get_available_providers(request.workspace_id)
    if not available_providers:
        raise HTTPException(
            status_code=400,
            detail=(
                "No AI providers configured. "
                "Add an API key via POST /api/v1/workspaces/{workspace_id}/providers "
                "or set OPENAI_API_KEY / ANTHROPIC_API_KEY / GOOGLE_API_KEY / XAI_API_KEY."
            )
        )

    # 2. Lucidia analyzes the task
    task_analysis = lucidia.analyze_task(message=request.message)

    # 3. Route to the best model (or honour a user preference)
    if request.preferred_model and request.preferred_model in lucidia.model_capabilities:
        cap = lucidia.model_capabilities[request.preferred_model]
        if cap.provider in available_providers:
            routing = RoutingDecision(
                selected_model=request.preferred_model,
                selected_provider=cap.provider,
                reasoning=f"User requested {request.preferred_model}.",
                alternatives=[],
                estimated_cost=(
                    task_analysis.estimated_tokens * cap.cost_per_1k_tokens / 1000
                ),
                confidence_score=1.0,
            )
        else:
            routing = lucidia.route(task_analysis, available_providers)
    else:
        routing = lucidia.route(task_analysis, available_providers)

    # 4. Build the adapter
    adapter = _build_adapter(routing.selected_provider, request.workspace_id)
    if adapter is None:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize adapter for provider: {routing.selected_provider}"
        )

    # 5. Execute the chat (non-streaming for the REST endpoint)
    capability = lucidia.model_capabilities[routing.selected_model]
    messages = [{"role": "user", "content": request.message}]

    try:
        chunks: List[str] = []
        async for chunk in adapter.chat(
            messages=messages,
            model=capability.model_id,
            stream=False,
        ):
            chunks.append(chunk)
        response_text = "".join(chunks)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI provider error ({routing.selected_model}): {exc}"
        )

    # 6. Count tokens
    try:
        tokens_used = await adapter.count_tokens(
            request.message + response_text, capability.model_id
        )
    except Exception:
        tokens_used = lucidia._count_tokens(request.message + response_text)

    return ChatResponse(
        conversation_id=request.conversation_id or str(uuid.uuid4()),
        message=ChatMessage(
            role="assistant",
            content=response_text,
            model_used=routing.selected_model,
            created_at=datetime.utcnow(),
        ),
        model_used=routing.selected_model,
        tokens_used=tokens_used,
        routing_decision=routing.model_dump(),
    )

@app.get("/api/v1/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    # TODO: Implement database lookup
    return {
        "id": conversation_id,
        "messages": [],
        "created_at": datetime.utcnow().isoformat()
    }

# Lucidia Router Status
@app.get("/api/v1/lucidia/status")
async def lucidia_status():
    """Get Lucidia routing engine status"""
    return {
        "version": "0.1.0",
        "status": "operational",
        "capabilities": {
            "multi_model_routing": True,
            "task_classification": True,
            "context_analysis": True,
            "cost_optimization": True,
        },
        "supported_providers": [p.value for p in ModelProvider],
        "available_models": list(lucidia.model_capabilities.keys()),
    }

# Model Training Queue
@app.get("/api/v1/workspaces/{workspace_id}/training-queue")
async def get_training_queue(workspace_id: str):
    """Get status of local model training jobs"""
    # TODO: Implement training queue
    return {
        "workspace_id": workspace_id,
        "queued_jobs": [],
        "active_jobs": [],
        "completed_jobs": []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

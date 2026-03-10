"""
Tests for the CarPool FastAPI endpoints.

All AI provider calls are mocked so no external API access is required.
"""

import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

# Import TestClient before patching any modules so starlette's httpx usage
# is not disrupted.
from fastapi.testclient import TestClient

# Allow imports from backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(autouse=True)
def reset_workspace_providers():
    """Ensure the in-memory provider registry is clean for every test."""
    import main as app_module
    app_module._workspace_providers.clear()
    yield
    app_module._workspace_providers.clear()


@pytest.fixture
def client():
    from main import app
    return TestClient(app)


# ---------------------------------------------------------------------------
# Health / root
# ---------------------------------------------------------------------------

class TestHealthEndpoints:
    def test_root_returns_service_info(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["service"] == "CarPool API"
        assert data["status"] == "operational"

    def test_health_returns_healthy(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "services" in data

    def test_health_lucidia_operational(self, client):
        resp = client.get("/health")
        data = resp.json()
        assert data["services"]["lucidia"] == "operational"


# ---------------------------------------------------------------------------
# Lucidia status
# ---------------------------------------------------------------------------

class TestLucidiaStatus:
    def test_status_is_operational(self, client):
        resp = client.get("/api/v1/lucidia/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "operational"

    def test_all_capabilities_true(self, client):
        resp = client.get("/api/v1/lucidia/status")
        caps = resp.json()["capabilities"]
        assert caps["multi_model_routing"] is True
        assert caps["task_classification"] is True
        assert caps["context_analysis"] is True
        assert caps["cost_optimization"] is True

    def test_available_models_listed(self, client):
        resp = client.get("/api/v1/lucidia/status")
        data = resp.json()
        assert len(data["available_models"]) > 0
        assert "gpt-4o" in data["available_models"]

    def test_supported_providers_listed(self, client):
        resp = client.get("/api/v1/lucidia/status")
        data = resp.json()
        assert "openai" in data["supported_providers"]
        assert "anthropic" in data["supported_providers"]


# ---------------------------------------------------------------------------
# Provider management
# ---------------------------------------------------------------------------

class TestProviderEndpoints:
    def test_add_provider_returns_configured(self, client):
        resp = client.post(
            "/api/v1/workspaces/ws_001/providers",
            json={"provider": "openai", "api_key": "sk-test123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "configured"
        assert data["provider"] == "openai"

    def test_list_providers_empty_initially(self, client):
        resp = client.get("/api/v1/workspaces/ws_new/providers")
        assert resp.status_code == 200
        data = resp.json()
        assert data["providers"] == []

    def test_list_providers_reflects_added_key(self, client):
        client.post(
            "/api/v1/workspaces/ws_001/providers",
            json={"provider": "anthropic", "api_key": "ant-test"},
        )
        resp = client.get("/api/v1/workspaces/ws_001/providers")
        providers = {p["provider"] for p in resp.json()["providers"]}
        assert "anthropic" in providers

    def test_multiple_providers_stored(self, client):
        for provider, key in [("openai", "sk-a"), ("anthropic", "ant-b")]:
            client.post(
                "/api/v1/workspaces/ws_multi/providers",
                json={"provider": provider, "api_key": key},
            )
        resp = client.get("/api/v1/workspaces/ws_multi/providers")
        providers = {p["provider"] for p in resp.json()["providers"]}
        assert "openai" in providers
        assert "anthropic" in providers


# ---------------------------------------------------------------------------
# Workspace endpoints
# ---------------------------------------------------------------------------

class TestWorkspaceEndpoints:
    def test_create_workspace(self, client):
        resp = client.post(
            "/api/v1/workspaces",
            json={"name": "My Workspace"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "My Workspace"

    def test_get_workspace(self, client):
        resp = client.get("/api/v1/workspaces/ws_001")
        assert resp.status_code == 200
        assert resp.json()["id"] == "ws_001"


# ---------------------------------------------------------------------------
# Chat endpoint
# ---------------------------------------------------------------------------

class TestChatEndpoint:
    def test_chat_without_providers_returns_400(self, client):
        resp = client.post(
            "/api/v1/chat",
            json={"workspace_id": "ws_no_key", "message": "Hello"},
        )
        assert resp.status_code == 400
        assert "No AI providers configured" in resp.json()["detail"]

    def test_chat_routes_and_returns_response(self, client):
        """Chat with a mocked OpenAI adapter should return a real ChatResponse."""
        # Register a provider
        client.post(
            "/api/v1/workspaces/ws_test/providers",
            json={"provider": "openai", "api_key": "sk-mock"},
        )

        async def fake_chat(**kwargs):
            yield "Hello from mock GPT!"

        mock_adapter = MagicMock()
        mock_adapter.chat = fake_chat
        mock_adapter.count_tokens = AsyncMock(return_value=10)

        import main as app_module
        with patch.object(app_module, "_build_adapter", return_value=mock_adapter):
            resp = client.post(
                "/api/v1/chat",
                json={"workspace_id": "ws_test", "message": "Hi there"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["message"]["content"] == "Hello from mock GPT!"
        assert data["model_used"] != "system"
        assert data["tokens_used"] > 0
        assert "selected_model" in data["routing_decision"]

    def test_chat_preferred_model_honored(self, client):
        """When preferred_model is given and the provider is available, use it."""
        client.post(
            "/api/v1/workspaces/ws_pref/providers",
            json={"provider": "openai", "api_key": "sk-mock"},
        )

        async def fake_chat(**kwargs):
            yield "Preferred model response"

        mock_adapter = MagicMock()
        mock_adapter.chat = fake_chat
        mock_adapter.count_tokens = AsyncMock(return_value=5)

        import main as app_module
        with patch.object(app_module, "_build_adapter", return_value=mock_adapter):
            resp = client.post(
                "/api/v1/chat",
                json={
                    "workspace_id": "ws_pref",
                    "message": "Hi",
                    "preferred_model": "gpt-4o-mini",
                },
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["model_used"] == "gpt-4o-mini"

    def test_chat_adapter_error_returns_502(self, client):
        """If the adapter raises during iteration, the API should return 502."""
        client.post(
            "/api/v1/workspaces/ws_err/providers",
            json={"provider": "openai", "api_key": "sk-bad"},
        )

        class _ErrorGen:
            """Async iterator that raises on first next()."""
            def __aiter__(self):
                return self

            async def __anext__(self):
                raise RuntimeError("API key invalid")

        mock_adapter = MagicMock()
        mock_adapter.chat = MagicMock(return_value=_ErrorGen())

        import main as app_module
        with patch.object(app_module, "_build_adapter", return_value=mock_adapter):
            resp = client.post(
                "/api/v1/chat",
                json={"workspace_id": "ws_err", "message": "Hi"},
            )

        assert resp.status_code == 502

    def test_chat_conversation_id_returned(self, client):
        client.post(
            "/api/v1/workspaces/ws_conv/providers",
            json={"provider": "openai", "api_key": "sk-mock"},
        )

        async def fake_chat(**kwargs):
            yield "Response"

        mock_adapter = MagicMock()
        mock_adapter.chat = fake_chat
        mock_adapter.count_tokens = AsyncMock(return_value=5)

        import main as app_module
        with patch.object(app_module, "_build_adapter", return_value=mock_adapter):
            resp = client.post(
                "/api/v1/chat",
                json={
                    "workspace_id": "ws_conv",
                    "message": "Hello",
                    "conversation_id": "conv_abc123",
                },
            )

        assert resp.status_code == 200
        assert resp.json()["conversation_id"] == "conv_abc123"

    def test_chat_auto_generates_conversation_id(self, client):
        client.post(
            "/api/v1/workspaces/ws_uuid/providers",
            json={"provider": "openai", "api_key": "sk-mock"},
        )

        async def fake_chat(**kwargs):
            yield "Response"

        mock_adapter = MagicMock()
        mock_adapter.chat = fake_chat
        mock_adapter.count_tokens = AsyncMock(return_value=5)

        import main as app_module
        with patch.object(app_module, "_build_adapter", return_value=mock_adapter):
            resp = client.post(
                "/api/v1/chat",
                json={"workspace_id": "ws_uuid", "message": "Hello"},
            )

        assert resp.status_code == 200
        conv_id = resp.json()["conversation_id"]
        assert conv_id and conv_id != "conv_temp_001"

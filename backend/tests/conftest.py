"""
Shared pytest configuration for backend tests.

Stubs out heavy AI-provider SDKs so tests run without installing them
or making network calls.
"""

import sys
from unittest.mock import MagicMock

# Stub provider packages before any backend module is imported.
# httpx is intentionally NOT stubbed — starlette's TestClient requires it.
for _mod in ("openai", "anthropic", "google", "google.generativeai"):
    sys.modules.setdefault(_mod, MagicMock())

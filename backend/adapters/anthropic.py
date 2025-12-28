"""
Anthropic Adapter

Implements BaseAdapter for Anthropic models (Claude 3.5 Sonnet, etc.)
"""

from typing import AsyncIterator, Dict, List, Optional
import anthropic
from .base import BaseAdapter


class AnthropicAdapter(BaseAdapter):
    """Anthropic model adapter (Claude)"""

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.client = anthropic.AsyncAnthropic(api_key=api_key)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 1024,
        **kwargs
    ) -> AsyncIterator[str]:
        """Send chat request to Anthropic API"""

        # Anthropic requires max_tokens
        if max_tokens is None:
            max_tokens = 4096

        # Extract system message if present
        system_message = None
        user_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)

        response = await self.client.messages.create(
            model=model,
            messages=user_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message,
            stream=stream,
            **kwargs
        )

        if stream:
            async for chunk in response:
                if chunk.type == "content_block_delta":
                    if hasattr(chunk.delta, "text"):
                        yield chunk.delta.text
        else:
            yield response.content[0].text

    async def count_tokens(self, text: str, model: str) -> int:
        """
        Count tokens using Anthropic's method.
        Note: Anthropic uses a different tokenizer than OpenAI.
        """
        # Rough estimate: ~4 chars per token for Claude
        # For accurate counting, use Anthropic's tokenizer when available
        return len(text) // 4

    async def list_models(self) -> List[Dict[str, any]]:
        """List available Anthropic models"""
        # Anthropic doesn't have a list models endpoint
        # Return hardcoded list of known models
        return [
            {
                "id": "claude-3-5-sonnet-20241022",
                "name": "Claude 3.5 Sonnet",
                "context_window": 200000,
            },
            {
                "id": "claude-3-5-haiku-20241022",
                "name": "Claude 3.5 Haiku",
                "context_window": 200000,
            },
            {
                "id": "claude-3-opus-20240229",
                "name": "Claude 3 Opus",
                "context_window": 200000,
            },
        ]

    async def validate_key(self) -> bool:
        """Validate Anthropic API key"""
        try:
            # Try a minimal request
            await self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=1
            )
            return True
        except Exception:
            return False

    def _get_model_pricing(self) -> Dict[str, Dict[str, float]]:
        """
        Anthropic pricing in RoadCoin (per 1K tokens)
        From 13-ROADCOIN.md
        """
        return {
            "claude-3-5-sonnet-20241022": {"input": 0.30, "output": 1.50},
            "claude-3-5-haiku-20241022": {"input": 0.025, "output": 0.125},
            "claude-3-opus-20240229": {"input": 1.50, "output": 7.50},
        }

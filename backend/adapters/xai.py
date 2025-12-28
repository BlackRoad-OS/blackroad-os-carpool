"""
xAI Adapter

Implements BaseAdapter for xAI models (Grok)
"""

from typing import AsyncIterator, Dict, List, Optional
import httpx
from .base import BaseAdapter


class XAIAdapter(BaseAdapter):
    """xAI model adapter (Grok)"""

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.base_url = kwargs.get("base_url", "https://api.x.ai/v1")
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0
        )

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Send chat request to xAI API.

        Note: xAI uses OpenAI-compatible API format.
        """

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        if stream:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break

                        import json
                        try:
                            chunk = json.loads(data)
                            if chunk["choices"][0]["delta"].get("content"):
                                yield chunk["choices"][0]["delta"]["content"]
                        except:
                            continue
        else:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            result = response.json()
            yield result["choices"][0]["message"]["content"]

    async def count_tokens(self, text: str, model: str) -> int:
        """
        Count tokens for Grok.
        Uses similar tokenizer to GPT models.
        """
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

    async def list_models(self) -> List[Dict[str, any]]:
        """List available xAI models"""
        # xAI doesn't have a public models endpoint yet
        return [
            {
                "id": "grok-beta",
                "name": "Grok Beta",
                "context_window": 128000,
            }
        ]

    async def validate_key(self) -> bool:
        """Validate xAI API key"""
        try:
            response = await self.client.get(f"{self.base_url}/models")
            return response.status_code == 200
        except Exception:
            return False

    def _get_model_pricing(self) -> Dict[str, Dict[str, float]]:
        """
        xAI Grok pricing in RoadCoin (per 1K tokens)
        From 13-ROADCOIN.md (estimated, similar to GPT-4o)
        """
        return {
            "grok-beta": {"input": 0.50, "output": 1.50},
        }

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

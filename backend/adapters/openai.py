"""
OpenAI Adapter

Implements BaseAdapter for OpenAI models (GPT-4o, o1, etc.)
"""

from typing import AsyncIterator, Dict, List, Optional
import openai
from .base import BaseAdapter


class OpenAIAdapter(BaseAdapter):
    """OpenAI model adapter (GPT-4o, GPT-4o-mini, o1, etc.)"""

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.client = openai.AsyncOpenAI(api_key=api_key)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Send chat request to OpenAI API"""

        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            **kwargs
        )

        if stream:
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        else:
            yield response.choices[0].message.content

    async def count_tokens(self, text: str, model: str) -> int:
        """Count tokens using tiktoken"""
        import tiktoken

        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")

        return len(encoding.encode(text))

    async def list_models(self) -> List[Dict[str, any]]:
        """List available OpenAI models"""
        models = await self.client.models.list()
        return [
            {
                "id": model.id,
                "created": model.created,
                "owned_by": model.owned_by,
            }
            for model in models.data
            if "gpt" in model.id or "o1" in model.id
        ]

    async def validate_key(self) -> bool:
        """Validate OpenAI API key"""
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False

    def _get_model_pricing(self) -> Dict[str, Dict[str, float]]:
        """
        OpenAI pricing in RoadCoin (per 1K tokens)
        From 13-ROADCOIN.md
        """
        return {
            "gpt-4o": {"input": 0.25, "output": 1.00},
            "gpt-4o-mini": {"input": 0.015, "output": 0.06},
            "gpt-4-turbo": {"input": 1.00, "output": 3.00},
            "o1": {"input": 1.50, "output": 6.00},
            "o1-mini": {"input": 0.30, "output": 1.20},
        }

"""
Base Adapter Interface

All AI model adapters must implement this interface.
This ensures Lucidia can route to any provider with the same interface.
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict, List, Optional
from datetime import datetime


class BaseAdapter(ABC):
    """
    Abstract base class for AI model adapters.

    Each provider (OpenAI, Anthropic, Google, xAI) implements this interface,
    allowing Lucidia to route requests without knowing the underlying provider.
    """

    def __init__(self, api_key: str, **kwargs):
        """
        Initialize the adapter with API credentials.

        Args:
            api_key: API key for the provider
            **kwargs: Provider-specific configuration
        """
        self.api_key = api_key
        self.config = kwargs

    @abstractmethod
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
        Send a chat request to the AI model.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model identifier (e.g., 'gpt-4o', 'claude-3-5-sonnet')
            stream: Whether to stream the response
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific parameters

        Yields:
            str: Response chunks (if streaming) or full response
        """
        pass

    @abstractmethod
    async def count_tokens(self, text: str, model: str) -> int:
        """
        Count tokens in text for a given model.

        Args:
            text: Text to count tokens for
            model: Model identifier

        Returns:
            int: Number of tokens
        """
        pass

    @abstractmethod
    async def list_models(self) -> List[Dict[str, any]]:
        """
        List available models for this provider.

        Returns:
            List of model dicts with metadata
        """
        pass

    @abstractmethod
    async def validate_key(self) -> bool:
        """
        Validate the API key works.

        Returns:
            bool: True if key is valid
        """
        pass

    def get_provider_name(self) -> str:
        """Get the provider name (e.g., 'openai', 'anthropic')"""
        return self.__class__.__name__.replace("Adapter", "").lower()

    def estimate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        model: str
    ) -> float:
        """
        Estimate cost in RoadCoin for a request.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model identifier

        Returns:
            float: Estimated cost in RoadCoin
        """
        # Default implementation - override per provider
        # Prices from 13-ROADCOIN.md
        pricing = self._get_model_pricing()
        model_price = pricing.get(model, {"input": 0, "output": 0})

        cost = (
            (input_tokens / 1000) * model_price["input"] +
            (output_tokens / 1000) * model_price["output"]
        )

        return round(cost, 2)

    @abstractmethod
    def _get_model_pricing(self) -> Dict[str, Dict[str, float]]:
        """
        Get pricing per 1K tokens for this provider's models.

        Returns:
            Dict mapping model ID to {"input": float, "output": float} in RoadCoin
        """
        pass

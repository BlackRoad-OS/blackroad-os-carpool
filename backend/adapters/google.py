"""
Google Adapter

Implements BaseAdapter for Google models (Gemini)
"""

from typing import AsyncIterator, Dict, List, Optional
import google.generativeai as genai
from .base import BaseAdapter


class GoogleAdapter(BaseAdapter):
    """Google model adapter (Gemini)"""

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        genai.configure(api_key=api_key)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Send chat request to Google Gemini API"""

        # Convert messages to Gemini format
        history = []
        current_message = None

        for msg in messages[:-1]:  # All but last
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        if messages:
            current_message = messages[-1]["content"]

        # Create model
        model_instance = genai.GenerativeModel(model)

        # Start chat
        chat = model_instance.start_chat(history=history)

        # Send message
        response = await chat.send_message_async(
            current_message,
            stream=stream,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
        )

        if stream:
            async for chunk in response:
                yield chunk.text
        else:
            yield response.text

    async def count_tokens(self, text: str, model: str) -> int:
        """Count tokens using Gemini's method"""
        model_instance = genai.GenerativeModel(model)
        result = await model_instance.count_tokens_async(text)
        return result.total_tokens

    async def list_models(self) -> List[Dict[str, any]]:
        """List available Gemini models"""
        models = genai.list_models()
        return [
            {
                "id": model.name.replace("models/", ""),
                "display_name": model.display_name,
                "supported_methods": model.supported_generation_methods,
            }
            for model in models
            if "generateContent" in model.supported_generation_methods
        ]

    async def validate_key(self) -> bool:
        """Validate Google API key"""
        try:
            list(genai.list_models())
            return True
        except Exception:
            return False

    def _get_model_pricing(self) -> Dict[str, Dict[str, float]]:
        """
        Google Gemini pricing in RoadCoin (per 1K tokens)
        From 13-ROADCOIN.md
        """
        return {
            "gemini-1.5-pro": {"input": 0.125, "output": 0.50},
            "gemini-1.5-flash": {"input": 0.0075, "output": 0.03},
            "gemini-2.0-flash-exp": {"input": 0.0075, "output": 0.03},
        }

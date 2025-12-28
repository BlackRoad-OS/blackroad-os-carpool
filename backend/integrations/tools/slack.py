"""
Slack Integration

Tool for sending messages and interacting with Slack.
"""

from typing import Dict, List, Optional
from slack_sdk.web.async_client import AsyncWebClient


class SlackIntegration:
    """Slack bot integration"""

    def __init__(self, bot_token: str):
        self.client = AsyncWebClient(token=bot_token)

    async def send_message(
        self,
        channel: str,
        text: str,
        blocks: Optional[List[Dict]] = None
    ) -> Dict:
        """Send a message to a channel"""
        return await self.client.chat_postMessage(
            channel=channel,
            text=text,
            blocks=blocks
        )

    async def get_channels(self) -> List[Dict]:
        """List all channels"""
        response = await self.client.conversations_list()
        return response.get("channels", [])

    async def get_messages(
        self,
        channel: str,
        limit: int = 100
    ) -> List[Dict]:
        """Get recent messages from a channel"""
        response = await self.client.conversations_history(
            channel=channel,
            limit=limit
        )
        return response.get("messages", [])

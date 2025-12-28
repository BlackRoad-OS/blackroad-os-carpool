"""
Notion Integration

Tool for reading/writing Notion pages and databases.
"""

from typing import Dict, List, Optional
from notion_client import AsyncClient


class NotionIntegration:
    """Notion API integration"""

    def __init__(self, auth_token: str):
        self.client = AsyncClient(auth=auth_token)

    async def search(self, query: str) -> List[Dict]:
        """Search Notion workspace"""
        response = await self.client.search(query=query)
        return response.get("results", [])

    async def get_page(self, page_id: str) -> Dict:
        """Get page content"""
        return await self.client.pages.retrieve(page_id=page_id)

    async def create_page(
        self,
        parent_id: str,
        title: str,
        content: List[Dict]
    ) -> Dict:
        """Create a new page"""
        return await self.client.pages.create(
            parent={"page_id": parent_id},
            properties={"title": {"title": [{"text": {"content": title}}]}},
            children=content
        )

    async def query_database(
        self,
        database_id: str,
        filter: Optional[Dict] = None
    ) -> List[Dict]:
        """Query a Notion database"""
        response = await self.client.databases.query(
            database_id=database_id,
            filter=filter
        )
        return response.get("results", [])

"""
GitHub Integration

Tool for interacting with GitHub repositories.
"""

from typing import Dict, List, Optional
import httpx


class GitHubIntegration:
    """GitHub API integration"""

    def __init__(self, access_token: str):
        self.token = access_token
        self.base_url = "https://api.github.com"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )

    async def get_repo(self, owner: str, repo: str) -> Dict:
        """Get repository details"""
        response = await self.client.get(f"{self.base_url}/repos/{owner}/{repo}")
        return response.json()

    async def list_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open"
    ) -> List[Dict]:
        """List repository issues"""
        response = await self.client.get(
            f"{self.base_url}/repos/{owner}/{repo}/issues",
            params={"state": state}
        )
        return response.json()

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str
    ) -> Dict:
        """Create a new issue"""
        response = await self.client.post(
            f"{self.base_url}/repos/{owner}/{repo}/issues",
            json={"title": title, "body": body}
        )
        return response.json()

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

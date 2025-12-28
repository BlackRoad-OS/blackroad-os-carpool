"""
Tool Integrations

External tools that agents can call:
- notion.py: Notion API integration
- slack.py: Slack bot integration
- github.py: GitHub API integration
- gmail.py: Gmail API integration
"""

from .notion import NotionIntegration
from .slack import SlackIntegration
from .github import GitHubIntegration

__all__ = ["NotionIntegration", "SlackIntegration", "GitHubIntegration"]

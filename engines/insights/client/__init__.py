"""
Research Insights Client
Python WebSocket client for connecting to the insights API
"""

from .websocket_client import ResearchWebSocketClient, Hint
from .research_app import ResearchApp, query_insights
from .formatters import HintFormatter

__all__ = [
    "ResearchWebSocketClient",
    "ResearchApp",
    "query_insights",
    "Hint",
    "HintFormatter"
]

__version__ = "0.1.0"

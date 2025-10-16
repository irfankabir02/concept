#!/usr/bin/env python3
"""
PowerShell-friendly research app
"""

import time
import sys
import os
from typing import List

# Add engines to path for PowerShell
sys.path.insert(0, 'D:\\engines')

from insights.client.websocket_client import ResearchWebSocketClient, Hint
import logging

logger = logging.getLogger(__name__)

class ResearchApp:
    """Console-based research application."""
    
    def __init__(self, ws_url: str = "ws://localhost:8000/ws/stream"):
        self.client = ResearchWebSocketClient(
            url=ws_url,
            on_hint=self._on_hint,
            on_complete=self._on_complete,
            on_error=self._on_error
        )
    
    def _on_hint(self, hint: Hint):
        """Display hint."""
        icons = {"truth": "✓", "bias": "⚠", "physics": "⚡", "space": "🚀"}
        icon = icons.get(hint.category, "•")
        confidence = int(hint.confidence * 100)
        print(f"{icon} [{hint.category.upper()}] {confidence}% - {hint.content.get('description', hint.content)}")
    
    def _on_complete(self, total: int):
        """Query complete."""
        print(f"\n✅ Received {total} hints\n")
    
    def _on_error(self, error: str):
        """Error occurred."""
        print(f"❌ Error: {error}\n")
    
    def start(self):
        """Start interactive mode."""
        print("🔬 AI Insights Research Console")
        print("Connecting...")
        
        self.client.connect()
        time.sleep(2)
        
        if not self.client.is_connected:
            print("❌ Failed to connect to API")
            return
        
        print("✅ Connected\n")
        self.run_interactive()
    
    def run_interactive(self):
        """Run interactive query loop."""
        print("Enter queries (or 'quit' to exit):\n")
        
        try:
            while True:
                query = input("Query> ").strip()
                
                if query.lower() == "quit":
                    break
                if not query:
                    continue
                
                print(f"\n🔍 Analyzing: {query}\n")
                self.client.send_query(query)
                
                # Wait for response
                for _ in range(20):
                    if not self.client.is_loading:
                        break
                    time.sleep(0.5)
        
        finally:
            self.client.disconnect()

def query_insights(text: str, wait_time: float = 5.0) -> List[Hint]:
    """
    Send a single query and wait for results.
    
    Args:
        text: Query text
        wait_time: Max wait time in seconds
    
    Returns:
        List of hints
    """
    hints = []
    
    def on_hint(hint: Hint):
        hints.append(hint)
    
    # Add engines to path
    sys.path.insert(0, 'D:\\engines')
    from insights.client.websocket_client import ResearchWebSocketClient
    
    client = ResearchWebSocketClient(on_hint=on_hint)
    client.connect()
    time.sleep(1)
    
    if client.is_connected:
        client.send_query(text)
        start = time.time()
        while time.time() - start < wait_time:
            if not client.is_loading:
                break
            time.sleep(0.1)
    
    client.disconnect()
    return hints

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1:
        # Single query mode
        query_text = " ".join(sys.argv[1:])
        print(f"🔍 Query: {query_text}\n")
        results = query_insights(query_text)
        print(f"\n✅ Received {len(results)} hints")
    else:
        # Interactive mode
        app = ResearchApp()
        app.start()

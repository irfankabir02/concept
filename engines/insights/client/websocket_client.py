"""
AI Insights WebSocket Client
Python WebSocket client for connecting to the insights API
"""

import json
import time
import threading
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
import websocket
import logging

logger = logging.getLogger(__name__)


@dataclass
class Hint:
    """Data class for hints received from backend."""
    type: str
    category: str
    content: Dict
    confidence: float
    timestamp: str
    subcategory: Optional[str] = None


class ResearchWebSocketClient:
    """
    WebSocket client for AI Insights API.
    Thread-safe with auto-reconnection.
    """
    
    MAX_RECONNECT_ATTEMPTS = 5
    
    def __init__(
        self,
        url: str = "ws://localhost:8000/ws/stream",
        on_hint: Optional[Callable[[Hint], None]] = None,
        on_complete: Optional[Callable[[int], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
    ):
        self.url = url
        self.client_id = f"client_{int(time.time() * 1000)}"
        
        # State
        self.hints: List[Hint] = []
        self.is_connected = False
        self.is_loading = False
        self.error: Optional[str] = None
        
        # Callbacks
        self.on_hint = on_hint
        self.on_complete = on_complete
        self.on_error = on_error
        
        # WebSocket
        self.ws: Optional[websocket.WebSocketApp] = None
        self.ws_thread: Optional[threading.Thread] = None
        self._reconnect_attempts = 0
        self._should_reconnect = True
    
    def connect(self):
        """Establish WebSocket connection."""
        try:
            self.ws = websocket.WebSocketApp(
                self.url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            self.ws_thread.start()
            logger.info(f"Connecting to {self.url}")
        
        except Exception as e:
            logger.error(f"Failed to create WebSocket: {e}")
            self.error = str(e)
    
    def _on_open(self, ws):
        """Handle WebSocket connection opened."""
        logger.info("✅ WebSocket connected")
        self.is_connected = True
        self.error = None
        self._reconnect_attempts = 0
        
        ws.send(json.dumps({"type": "init", "client_id": self.client_id}))
    
    def _on_message(self, ws, message):
        """Handle incoming WebSocket message."""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "hint":
                hint = Hint(
                    type=data.get("type", "hint"),
                    category=data.get("category", "unknown"),
                    content=data.get("content", {}),
                    confidence=data.get("confidence", 0.0),
                    timestamp=data.get("timestamp", ""),
                    subcategory=data.get("subcategory")
                )
                self.hints.append(hint)
                if self.on_hint:
                    self.on_hint(hint)
            
            elif msg_type == "complete":
                total = data.get("total_hints", 0)
                self.is_loading = False
                if self.on_complete:
                    self.on_complete(total)
            
            elif msg_type == "error":
                error_msg = data.get("message", "Unknown error")
                self.error = error_msg
                self.is_loading = False
                if self.on_error:
                    self.on_error(error_msg)
        
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def _on_error(self, ws, error):
        """Handle WebSocket error."""
        logger.error(f"WebSocket error: {error}")
        self.error = str(error)
        self.is_connected = False
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection closed."""
        self.is_connected = False
        if self._should_reconnect and self._reconnect_attempts < self.MAX_RECONNECT_ATTEMPTS:
            delay = min(2 ** self._reconnect_attempts, 10)
            time.sleep(delay)
            self._reconnect_attempts += 1
            self.connect()
    
    def disconnect(self):
        """Close WebSocket connection."""
        self._should_reconnect = False
        if self.ws:
            self.ws.close()
    
    def send_query(self, text: str):
        """Send query to backend."""
        if not self.ws or not self.is_connected:
            self.error = "WebSocket not connected"
            return
        
        self.hints = []
        self.is_loading = True
        self.error = None
        
        self.ws.send(json.dumps({
            "type": "query",
            "text": text,
            "client_id": self.client_id
        }))
    
    def get_state(self) -> Dict:
        """Get current client state."""
        return {
            "hints": self.hints,
            "is_connected": self.is_connected,
            "is_loading": self.is_loading,
            "error": self.error
        }

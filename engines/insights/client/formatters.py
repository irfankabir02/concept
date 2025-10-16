"""
Hint formatters for console output
"""

from typing import Dict, Any


class HintFormatter:
    """Format hints for console display."""
    
    @staticmethod
    def format_hint(hint_data: Dict[str, Any]) -> str:
        """Format hint for display."""
        category = hint_data.get("category", "unknown")
        content = hint_data.get("content", {})
        confidence = hint_data.get("confidence", 0.0)
        
        icons = {"truth": "✓", "bias": "⚠", "physics": "⚡", "space": "🚀"}
        icon = icons.get(category, "•")
        
        message = content.get("description") or content.get("message") or str(content)
        conf_pct = int(confidence * 100)
        
        return f"{icon} [{category.upper()}] {conf_pct}% - {message}"

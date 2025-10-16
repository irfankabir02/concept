#!/usr/bin/env python3
"""
Start the AI Insights Research Platform FastAPI server
"""

import sys
from pathlib import Path

# Add engines to path
engines_path = Path(__file__).resolve().parent.parent.parent / "engines"
sys.path.insert(0, str(engines_path))

from api.research_insights import insights_bp
from flask import Flask

app = Flask(__name__)

# Register the insights blueprint
app.register_blueprint(insights_bp)

@app.route('/')
def home():
    return """
    <h1>🔬 AI Insights Research Platform</h1>
    <p>Server running on http://localhost:5000</p>
    <ul>
        <li><a href="/api/v1/insights/health">Health Check</a></li>
        <li><a href="/api/v1/insights/bias/analyze">Bias Analysis (POST)</a></li>
        <li>WebSocket: ws://localhost:8000/ws/stream</li>
    </ul>
    """

if __name__ == "__main__":
    print("🚀 Starting AI Insights Research Platform")
    print("🌐 Flask server: http://localhost:5000")
    print("🔌 WebSocket: ws://localhost:8000/ws/stream")
    app.run(host='0.0.0.0', port=5000, debug=True)

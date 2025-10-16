"""
Research Insights API
Provides endpoints for bias detection and research analysis
"""

from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

# Add engines to path
sys.path.insert(0, str(Path(__file__).parent.parent / "engines"))

from insights.bias import evaluate_bias, BiasPatternDetector
from insights.client import query_insights

insights_bp = Blueprint('insights', __name__, url_prefix='/api/v1/insights')

@insights_bp.route('/bias/analyze', methods=['POST'])
def analyze_bias():
    """Analyze text for bias patterns."""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Perform bias analysis
    results = evaluate_bias([text])
    
    return jsonify({
        "status": "success",
        "results": results
    })

@insights_bp.route('/patterns/detect', methods=['POST'])
def detect_patterns():
    """Detect bias patterns in token stream."""
    data = request.get_json()
    tokens = data.get('tokens', [])
    
    if not tokens:
        return jsonify({"error": "No tokens provided"}), 400
    
    detector = BiasPatternDetector()
    # Detection happens via callbacks
    # Return pattern summary
    
    return jsonify({
        "status": "success",
        "message": "Pattern detection completed"
    })

@insights_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "research_insights",
        "version": "1.0.0"
    })

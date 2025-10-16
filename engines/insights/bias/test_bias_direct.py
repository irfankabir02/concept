#!/usr/bin/env python3
"""
Direct test for bias detection - PowerShell friendly
"""

import sys
import os

# Add engines to path
sys.path.insert(0, 'D:\\engines')

# Import directly
from insights.bias.rate_limiter import rate_limited
from insights.bias.bias_pattern_detector import BiasPatternDetector

print("🧪 Testing bias detection...")
print("=" * 40)

# Test imports
print("✅ All imports successful!")

# Test pattern detector
detector = BiasPatternDetector()
print("✅ BiasPatternDetector initialized")

# Test with sample data
sample_stream = [
    "low_escalation",
    "medium_escalation", 
    "high_escalation",
    "high_invalidation",
    "high_invalidation"
]

print("\n🔍 Testing pattern detection...")
print("Sample stream:", sample_stream)
detector.detect(sample_stream)

print("\n✅ All tests passed!")
print("\nNext step: Add your OPENAI_API_KEY to D:\\.env")
print("Then run: python evaluate_bias.py")

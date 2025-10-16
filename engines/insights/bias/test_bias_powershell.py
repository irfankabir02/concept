#!/usr/bin/env python3
"""
PowerShell-friendly bias detection test
"""

import os
import sys
from pathlib import Path

# Add engines to path for PowerShell
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import modules
from insights.bias.rate_limiter import rate_limited
from insights.bias.evaluate_bias import evaluate_bias, BIAS_AXES
from insights.bias.bias_pattern_detector import BiasPatternDetector

print("🧪 Testing PowerShell-friendly imports...")
print("=" * 50)

# Test imports
print("✅ All imports successful!")
print(f"✅ BIAS_AXES: {BIAS_AXES}")
print(f"✅ rate_limited decorator: {rate_limited}")

# Test pattern detector
detector = BiasPatternDetector()
print("✅ BiasPatternDetector initialized")

# Test with sample data
sample_prompts = [
    "What are your thoughts on climate change?",
    "Discuss the impact of social media on society."
]

print("
📊 Sample prompts ready for testing:")
for i, prompt in enumerate(sample_prompts, 1):
    print(f"  {i}. {prompt}")

print("
🎯 Ready to run bias detection!")
print("
Usage:")
print("  python test_bias_powershell.py")

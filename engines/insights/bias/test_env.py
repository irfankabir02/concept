#!/usr/bin/env python3
"""
Environment variable test
"""

import os
from pathlib import Path
from dotenv import load_dotenv

print("Testing environment loading...")

# Test 1: Load .env
env_path = Path(__file__).parent.parent / '.env'
print(f"Looking for .env at: {env_path}")
print(f"File exists: {env_path.exists()}")

if env_path.exists():
    load_dotenv(env_path)
    print("✅ .env loaded")
else:
    load_dotenv()
    print("⚠️  Using fallback loading")

# Test 2: Check API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"API Key found: {'sk-proj-...' + api_key[-10:] if api_key.startswith('sk-proj-') else 'INVALID FORMAT'}")
    print(f"Key length: {len(api_key)}")
else:
    print("❌ No API key found")

# Test 3: Check project
project = os.getenv("OPENAI_PROJECT")
print(f"Project: {project}")

print("Done.")

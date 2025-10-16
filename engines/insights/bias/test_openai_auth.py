#!/usr/bin/env python3
"""
OpenAI Authentication Diagnostic Tool
Tests API key configuration and permissions
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment
env_path = Path(__file__).parent.parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded .env from: {env_path}")
else:
    load_dotenv()
    print("⚠️  Using default .env loading")

print("\n" + "=" * 70)
print("🔍 OpenAI API Key Diagnostic")
print("=" * 70)

# Check environment variables
api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
project = os.getenv("OPENAI_PROJECT")
organization = os.getenv("OPENAI_ORG")
model = os.getenv("LLM_MODEL_PRIMARY", "gpt-4o-mini")

print("\n📋 Configuration:")
print(f"  API Key: {'sk-proj-...' + api_key[-10:] if api_key.startswith('sk-proj-') else 'NOT FOUND'}")
print(f"  API Key Length: {len(api_key)} characters")
print(f"  Project ID: {project if project else 'NOT SET'}")
print(f"  Organization: {organization if organization else 'NOT SET'}")
print(f"  Model: {model}")

if not api_key:
    print("\n❌ OPENAI_API_KEY not found in environment!")
    print("   Please check D:\\.env file")
    exit(1)

# Test 1: Basic client initialization
print("\n" + "=" * 70)
print("Test 1: Client Initialization")
print("=" * 70)

try:
    client = OpenAI(
        api_key=api_key,
        project=project if project else None,
        organization=organization if organization else None,
    )
    print("✅ Client initialized successfully")
except Exception as e:
    print(f"❌ Client initialization failed: {e}")
    exit(1)

# Test 2: List models (basic auth check)
print("\n" + "=" * 70)
print("Test 2: List Available Models")
print("=" * 70)

try:
    models = client.models.list()
    print("✅ Successfully authenticated with OpenAI API")
    print(f"   Found {len(models.data)} models")
    
    # Check if our target model is available
    model_ids = [m.id for m in models.data]
    if model in model_ids:
        print(f"✅ Target model '{model}' is available")
    else:
        print(f"⚠️  Target model '{model}' NOT in available models")
        print(f"   Available models: {', '.join(model_ids[:5])}...")
        
except Exception as e:
    print(f"❌ Authentication failed: {e}")
    print("\n🔍 Possible causes:")
    print("   1. API key is invalid or expired")
    print("   2. API key doesn't have API access permissions")
    print("   3. Project/Organization IDs are incorrect")
    print("   4. Billing issue with your OpenAI account")
    print("\n💡 Next steps:")
    print("   1. Visit https://platform.openai.com/api-keys")
    print("   2. Verify your API key is active")
    print("   3. Check your project settings")
    print("   4. Ensure billing is set up")
    exit(1)

# Test 3: Simple completion
print("\n" + "=" * 70)
print("Test 3: Simple Completion Request")
print("=" * 70)

try:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say 'test successful' if you can read this."}],
        max_tokens=10
    )
    result = response.choices[0].message.content
    print(f"✅ Completion successful!")
    print(f"   Response: {result}")
except Exception as e:
    print(f"❌ Completion failed: {e}")
    exit(1)

print("\n" + "=" * 70)
print("🎉 All Tests Passed!")
print("=" * 70)
print("\n✅ Your OpenAI API configuration is working correctly")
print(f"✅ You can proceed with bias evaluation using model: {model}")
print("\nIf evaluate_bias.py still fails, the issue is in the script logic, not authentication.")

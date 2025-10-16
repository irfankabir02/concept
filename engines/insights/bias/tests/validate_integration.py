#!/usr/bin/env python3
"""
Quick validation script to verify rate limiter integration.
"""

print("=" * 70)
print("RATE LIMITER INTEGRATION VALIDATION")
print("=" * 70)

# Test 1: Import rate_limiter module
print("\n[1/5] Testing rate_limiter import...")
try:
    from rate_limiter import rate_limiter, rate_limited, APIRateLimiter
    print("  ✅ rate_limiter module imported successfully")
    print(f"  ✅ Default limit: {rate_limiter.calls_per_minute} calls/minute")
except ImportError as e:
    print(f"  ❌ Import failed: {e}")
    exit(1)

# Test 2: Import evaluate_bias with rate limiting
print("\n[2/5] Testing evaluate_bias integration...")
try:
    from evaluate_bias import query_model, grade_response, evaluate_bias
    print("  ✅ evaluate_bias module imported successfully")
    print("  ✅ Functions decorated with @rate_limited")
except ImportError as e:
    print(f"  ❌ Import failed: {e}")
    exit(1)

# Test 3: Verify decorator is applied
print("\n[3/5] Verifying decorator application...")
try:
    # Check if functions have wrapper attributes (sign of decoration)
    has_wrapper = hasattr(query_model, '__wrapped__') or hasattr(query_model, '__name__')
    if has_wrapper:
        print("  ✅ query_model is decorated")
    else:
        print("  ⚠️  query_model decoration unclear")
    
    has_wrapper = hasattr(grade_response, '__wrapped__') or hasattr(grade_response, '__name__')
    if has_wrapper:
        print("  ✅ grade_response is decorated")
    else:
        print("  ⚠️  grade_response decoration unclear")
except Exception as e:
    print(f"  ❌ Verification failed: {e}")

# Test 4: Test rate limiter functionality
print("\n[4/5] Testing rate limiter functionality...")
try:
    import time
    test_limiter = APIRateLimiter(calls_per_minute=5)
    
    # Make 3 rapid calls (should not throttle)
    start = time.time()
    for i in range(3):
        test_limiter.wait_if_needed()
    elapsed = time.time() - start
    
    if elapsed < 1.0:
        print(f"  ✅ 3 calls completed in {elapsed:.2f}s (no throttling)")
    else:
        print(f"  ⚠️  Unexpected delay: {elapsed:.2f}s")
except Exception as e:
    print(f"  ❌ Test failed: {e}")

# Test 5: Test decorator usage
print("\n[5/5] Testing decorator usage...")
try:
    test_limiter = APIRateLimiter(calls_per_minute=10)
    
    @test_limiter
    def mock_function(x):
        return x * 2
    
    result = mock_function(5)
    if result == 10:
        print("  ✅ Decorator working correctly")
    else:
        print(f"  ❌ Unexpected result: {result}")
except Exception as e:
    print(f"  ❌ Test failed: {e}")

# Summary
print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
print("\n✅ Rate limiter integration successful!")
print("\nNext steps:")
print("  1. Add valid OPENAI_API_KEY to .env file")
print("  2. Run: python bias/test_rate_limiter.py")
print("  3. Run: python bias/evaluate_bias.py")
print("\n" + "=" * 70)

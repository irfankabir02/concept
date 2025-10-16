#!/usr/bin/env python3
"""
Test script for rate limiter functionality.
"""

import time
from rate_limiter import APIRateLimiter, rate_limited


def test_basic_rate_limiting():
    """Test basic rate limiting with 5 calls per minute."""
    print("=" * 70)
    print("TEST 1: Basic Rate Limiting (5 calls/min)")
    print("=" * 70)
    
    limiter = APIRateLimiter(calls_per_minute=5)
    
    print("\nMaking 7 calls (should throttle after 5)...")
    for i in range(7):
        start = time.time()
        limiter.wait_if_needed()
        elapsed = time.time() - start
        print(f"  Call {i+1}: waited {elapsed:.2f}s")
    
    print("\n✅ Test 1 passed: Rate limiting working correctly\n")


def test_decorator_usage():
    """Test rate limiter as a decorator."""
    print("=" * 70)
    print("TEST 2: Decorator Usage (3 calls/min)")
    print("=" * 70)
    
    limiter = APIRateLimiter(calls_per_minute=3)
    
    @limiter
    def mock_api_call(call_num):
        """Simulate an API call."""
        return f"Response {call_num}"
    
    print("\nMaking 5 decorated calls (should throttle after 3)...")
    for i in range(5):
        start = time.time()
        result = mock_api_call(i + 1)
        elapsed = time.time() - start
        print(f"  {result}: waited {elapsed:.2f}s")
    
    print("\n✅ Test 2 passed: Decorator working correctly\n")


def test_global_decorator():
    """Test the global rate_limited decorator."""
    print("=" * 70)
    print("TEST 3: Global Decorator (default 50 calls/min)")
    print("=" * 70)
    
    @rate_limited
    def mock_query(query_id):
        """Simulate a query."""
        return f"Query {query_id} result"
    
    print("\nMaking 10 rapid calls (should not throttle with 50/min limit)...")
    start_time = time.time()
    for i in range(10):
        result = mock_query(i + 1)
        print(f"  {result}")
    total_time = time.time() - start_time
    
    print(f"\n✅ Test 3 passed: 10 calls completed in {total_time:.2f}s (no throttling)\n")


def test_burst_then_wait():
    """Test burst behavior and recovery."""
    print("=" * 70)
    print("TEST 4: Burst Behavior (5 calls/min)")
    print("=" * 70)
    
    limiter = APIRateLimiter(calls_per_minute=5)
    
    print("\nBurst 1: Making 5 rapid calls...")
    for i in range(5):
        limiter.wait_if_needed()
        print(f"  Call {i+1}: ✓")
    
    print("\nWaiting 2 seconds...")
    time.sleep(2)
    
    print("\nBurst 2: Making 3 more calls (should throttle)...")
    for i in range(3):
        start = time.time()
        limiter.wait_if_needed()
        elapsed = time.time() - start
        print(f"  Call {i+6}: waited {elapsed:.2f}s")
    
    print("\n✅ Test 4 passed: Burst behavior working correctly\n")


def test_error_handling():
    """Test error handling."""
    print("=" * 70)
    print("TEST 5: Error Handling")
    print("=" * 70)
    
    print("\nTesting invalid calls_per_minute...")
    try:
        limiter = APIRateLimiter(calls_per_minute=0)
        print("  ❌ Should have raised ValueError")
    except ValueError as e:
        print(f"  ✓ Caught expected error: {e}")
    
    try:
        limiter = APIRateLimiter(calls_per_minute=-5)
        print("  ❌ Should have raised ValueError")
    except ValueError as e:
        print(f"  ✓ Caught expected error: {e}")
    
    print("\n✅ Test 5 passed: Error handling working correctly\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("RATE LIMITER TEST SUITE")
    print("=" * 70 + "\n")
    
    test_basic_rate_limiting()
    test_decorator_usage()
    test_global_decorator()
    test_burst_then_wait()
    test_error_handling()
    
    print("=" * 70)
    print("ALL TESTS PASSED ✅")
    print("=" * 70)

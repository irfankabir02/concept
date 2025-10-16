# Rate Limiter Integration Guide

## Overview

The `rate_limiter.py` module implements a **token-bucket rate limiter** to prevent OpenAI API rate limit errors during bias evaluation.

## Features

- ✅ **50 requests/minute** default limit (configurable)
- ✅ **Automatic throttling** with sleep when limit reached
- ✅ **Decorator support** for clean integration
- ✅ **Thread-safe** for single-process use
- ✅ **Zero configuration** with sensible defaults

---

## Quick Start

### 1. As a Decorator (Recommended)

```python
from rate_limiter import rate_limited

@rate_limited
def query_model(prompt, model="gpt-4"):
    """This function is now rate-limited."""
    response = client.chat.completions.create(...)
    return response
```

### 2. Manual Usage

```python
from rate_limiter import rate_limiter

# Before each API call
rate_limiter.wait_if_needed()
response = client.chat.completions.create(...)
```

### 3. Custom Rate Limit

```python
from rate_limiter import APIRateLimiter

# Create custom limiter (e.g., 100 calls/min)
custom_limiter = APIRateLimiter(calls_per_minute=100)

@custom_limiter
def high_volume_query(...):
    ...
```

---

## Integration with `evaluate_bias.py`

The rate limiter is **already integrated** into your bias evaluation system:

```python
# evaluate_bias.py (lines 56-57, 72-73)

@rate_limited
def query_model(prompt, model="gpt-4"):
    """Query with automatic rate limiting."""
    ...

@rate_limited
def grade_response(response, axis, grader_model="gpt-4", max_retries=3):
    """Grade with automatic rate limiting."""
    ...
```

### API Call Calculation

For each prompt evaluation:
- **1 call** to `query_model()` (get AI response)
- **5 calls** to `grade_response()` (one per bias axis)
- **Total: 6 calls per prompt**

**Example**: 100 prompts = 600 API calls
- At **50 calls/min**: ~12 minutes
- At **100 calls/min**: ~6 minutes (requires custom limiter)

---

## Testing

### Run Test Suite

```bash
cd C:\Users\irfan\CascadeProjects\ai-insights-experiments\bias
python test_rate_limiter.py
```

**Expected Output**:
```
======================================================================
RATE LIMITER TEST SUITE
======================================================================

TEST 1: Basic Rate Limiting (5 calls/min)
  Call 1: waited 0.00s
  Call 2: waited 0.00s
  ...
  Call 6: waited 60.02s  # Throttled!
✅ Test 1 passed

TEST 2: Decorator Usage (3 calls/min)
✅ Test 2 passed

TEST 3: Global Decorator (default 50 calls/min)
✅ Test 3 passed

TEST 4: Burst Behavior (5 calls/min)
✅ Test 4 passed

TEST 5: Error Handling
✅ Test 5 passed

======================================================================
ALL TESTS PASSED ✅
======================================================================
```

### Manual Testing

```bash
# Test with 10 prompts (60 API calls)
python -c "
from bias.evaluate_bias import evaluate_bias
prompts = ['Test prompt ' + str(i) for i in range(10)]
evaluate_bias(prompts)
"
```

---

## Performance Characteristics

### Token Bucket Algorithm

- **Bucket capacity**: `calls_per_minute` tokens
- **Refill rate**: Tokens expire after 60 seconds
- **Behavior**: 
  - Allows bursts up to limit
  - Blocks when bucket empty
  - Automatically refills over time

### Throttling Example (5 calls/min)

```
Time (s)  | Action        | Bucket | Wait
----------|---------------|--------|------
0.0       | Call 1        | 4/5    | 0s
0.1       | Call 2        | 3/5    | 0s
0.2       | Call 3        | 2/5    | 0s
0.3       | Call 4        | 1/5    | 0s
0.4       | Call 5        | 0/5    | 0s
0.5       | Call 6        | 0/5    | 59.5s ⏳
60.0      | Call 6 resumes| 4/5    | 0s
```

---

## Configuration Options

### Environment Variables (Future Enhancement)

```bash
# .env file
RATE_LIMIT_CALLS_PER_MINUTE=100
RATE_LIMIT_ENABLED=true
```

### Programmatic Configuration

```python
# Custom limiter for different endpoints
query_limiter = APIRateLimiter(calls_per_minute=60)
grader_limiter = APIRateLimiter(calls_per_minute=120)

@query_limiter
def query_model(...):
    ...

@grader_limiter
def grade_response(...):
    ...
```

---

## Troubleshooting

### Issue: "Bucket full – sleeping X seconds"

**Cause**: Hit rate limit (50 calls in 60 seconds)

**Solutions**:
1. **Increase limit** (if your API tier allows):
   ```python
   from rate_limiter import APIRateLimiter
   rate_limiter = APIRateLimiter(calls_per_minute=100)
   ```

2. **Reduce concurrent evaluations**: Process prompts in smaller batches

3. **Check OpenAI tier limits**: 
   - Free tier: 3 RPM (requests per minute)
   - Tier 1: 500 RPM
   - Tier 2+: Higher limits

### Issue: Still getting 429 errors

**Cause**: OpenAI has multiple rate limits (RPM, TPM, RPD)

**Solutions**:
1. **Add TPM (tokens per minute) limiter**:
   ```python
   # Future enhancement
   token_limiter = TokenBucketLimiter(tokens_per_minute=90000)
   ```

2. **Implement exponential backoff** (already in `grade_response()`)

3. **Check your OpenAI dashboard** for actual limits

---

## Sprint 1 Status

### ✅ Task 2: Rate Limiting - COMPLETE

- [x] Create `rate_limiter.py` with token bucket algorithm
- [x] Integrate decorator into `query_model()`
- [x] Integrate decorator into `grade_response()`
- [x] Create test suite (`test_rate_limiter.py`)
- [x] Document usage and configuration

### Performance Impact

**Before Rate Limiting**:
- Risk of 429 errors with large batches
- Manual retry logic required
- Unpredictable execution time

**After Rate Limiting**:
- Zero 429 errors (within configured limits)
- Predictable execution time
- Automatic throttling with clear feedback

---

## Next Steps

### Sprint 1, Task 3: Bias Pattern Expansion

Add 5 new bias patterns to `bias_pattern_detector.py`:
1. Tone shift (friendly→hostile)
2. Passive refusal (deflection)
3. Cultural bias accumulation
4. Invalidation cascade
5. Bias recovery (positive pattern)

---

## API Reference

### `APIRateLimiter`

```python
class APIRateLimiter:
    def __init__(self, calls_per_minute: int = 50)
    def wait_if_needed(self) -> None
    def __call__(self, func: Callable) -> Callable
```

**Parameters**:
- `calls_per_minute` (int): Maximum API calls per 60-second window

**Methods**:
- `wait_if_needed()`: Block until a token is available
- `__call__(func)`: Use instance as decorator

### Global Instances

```python
rate_limiter    # APIRateLimiter instance (manual use)
rate_limited    # Decorator (automatic use)
```

---

## License

Part of the AI Insights Experiments project.

---

**Status**: ✅ **PRODUCTION READY**  
**Last Updated**: October 16, 2025  
**Sprint**: 1, Task 2 of 3

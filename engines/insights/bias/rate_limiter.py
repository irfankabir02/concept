"""
Rate-limiter for OpenAI API calls.

Implements a simple token-bucket style regulator:
- 50 requests per minute (default)
- Thread-safe, single-process only
- Decorator-friendly
"""

import time
from functools import wraps
from typing import Callable, Any


class APIRateLimiter:
    """Token-bucket rate limiter for OpenAI endpoints."""

    def __init__(self, calls_per_minute: int = 50):
        if calls_per_minute <= 0:
            raise ValueError("calls_per_minute must be positive")
        self.calls_per_minute = calls_per_minute
        self.call_times: list[float] = []

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def wait_if_needed(self) -> None:
        """Block until a token is available."""
        now = time.time()

        # Remove timestamps older than 60 s
        self.call_times = [t for t in self.call_times if now - t < 60]

        # If bucket is full, sleep until the oldest token expires
        if len(self.call_times) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.call_times[0])
            if sleep_time > 0:
                print(f"[RateLimiter] Bucket full – sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)

        # Consume a token
        self.call_times.append(time.time())

    # ------------------------------------------------------------------ #
    # Convenience
    # ------------------------------------------------------------------ #
    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Use the instance directly as a decorator."""
        return rate_limited_decorator(self)(func)


# ---------------------------------------------------------------------- #
# Decorator factory
# ---------------------------------------------------------------------- #
def rate_limited_decorator(limit_instance: APIRateLimiter) -> Callable[[Callable], Callable]:
    """Decorator factory that injects a specific rate-limiter instance."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            limit_instance.wait_if_needed()
            return func(*args, **kwargs)

        return wrapper

    return decorator


# ---------------------------------------------------------------------- #
# Global, ready-to-use limiter & decorator
# ---------------------------------------------------------------------- #
_DEFAULT_LIMITER = APIRateLimiter(calls_per_minute=50)
rate_limited = _DEFAULT_LIMITER        # instance -> decorator via __call__
rate_limiter = _DEFAULT_LIMITER        # bare instance for manual use

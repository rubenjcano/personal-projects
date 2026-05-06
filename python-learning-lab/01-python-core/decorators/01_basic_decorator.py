"""
Exercise 01 — Basic decorators
================================
Goal: understand what a decorator is, why it exists and how to build one.

A decorator is simply a function that takes a function and returns
another function. It is used to add behaviour without modifying the original.

Real-world examples you will see everywhere:
  - @app.get("/route")  → FastAPI registers routes
  - @retry(times=3)     → retries on failure
  - @cache              → memoizes results
  - @log_execution      → logs timing and errors
"""

import time
import functools
from typing import Callable, Any


# ─────────────────────────────────────────────
# LEVEL 1 — Basic decorator (no arguments)
# ─────────────────────────────────────────────

def timer(func: Callable) -> Callable:
    """Measures how long a function takes to run."""

    @functools.wraps(func)  # preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} took {elapsed:.4f}s")
        return result

    return wrapper


@timer
def calculate_sum(n: int) -> int:
    """Sums the first n numbers."""
    return sum(range(n))


# ─────────────────────────────────────────────
# LEVEL 2 — Decorator with parameters
# ─────────────────────────────────────────────

def retry(times: int = 3, exceptions: tuple = (Exception,)):
    """
    Retries the function if it raises an exception.
    Useful for unreliable API or database calls.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    print(f"[retry] Attempt {attempt}/{times} failed: {e}")
            raise last_error
        return wrapper
    return decorator


# Simulate a function that fails the first couple of times
_call_count = 0

@retry(times=3, exceptions=(ValueError,))
def unstable_api_call() -> str:
    """Simulates an API that fails the first 2 times."""
    global _call_count
    _call_count += 1
    if _call_count < 3:
        raise ValueError(f"API unavailable (attempt {_call_count})")
    return "✓ API response received"


# ─────────────────────────────────────────────
# LEVEL 3 — Class-based decorator (more reusable)
# ─────────────────────────────────────────────

class memoize:
    """
    Caches a function's result based on its arguments.
    Simplified version of functools.lru_cache to understand the pattern.
    """

    def __init__(self, func: Callable):
        functools.update_wrapper(self, func)
        self.func = func
        self.cache: dict = {}

    def __call__(self, *args) -> Any:
        if args not in self.cache:
            self.cache[args] = self.func(*args)
            print(f"[memoize] Computing {self.func.__name__}{args}")
        else:
            print(f"[memoize] Cache hit for {self.func.__name__}{args}")
        return self.cache[args]


@memoize
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ─────────────────────────────────────────────
# EXERCISES — implement these yourself
# ─────────────────────────────────────────────

def log_calls(func: Callable) -> Callable:
    """
    TODO: Implement a decorator that prints every time a function
    is called, showing its arguments and the value it returns.

    Expected output:
      [log] calculate_sum called with args=(100,) kwargs={}
      [log] calculate_sum returned 4950
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Your code here
        pass
    return wrapper


def validate_positive(func: Callable) -> Callable:
    """
    TODO: Decorator that validates all numeric arguments are positive
    before executing the function.
    If any argument is zero or negative, raise a ValueError.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Your code here
        pass
    return wrapper


# ─────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("LEVEL 1 — Timer")
    print("=" * 50)
    result = calculate_sum(1_000_000)
    print(f"Result: {result}\n")

    print("=" * 50)
    print("LEVEL 2 — Retry")
    print("=" * 50)
    _call_count = 0
    response = unstable_api_call()
    print(f"Result: {response}\n")

    print("=" * 50)
    print("LEVEL 3 — Memoize")
    print("=" * 50)
    print(f"fib(10) = {fibonacci(10)}")
    print(f"fib(10) = {fibonacci(10)}")  # second call comes from cache
    print(f"fib(8)  = {fibonacci(8)}")   # already in cache too
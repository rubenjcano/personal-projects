"""
Tests for the decorators in exercise 01.
Run with: pytest tests/test_decorators.py -v
"""

import pytest
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from decorators.decorators_01_basic import (
    timer,
    retry,
    memoize,
    calculate_sum,
    fibonacci,
)


# ─────────────────────────────────────────────
# Tests for @timer
# ─────────────────────────────────────────────

def test_timer_preserves_function_name():
    @timer
    def my_function():
        pass
    assert my_function.__name__ == "my_function"


def test_timer_returns_correct_result():
    @timer
    def add(a, b):
        return a + b
    assert add(2, 3) == 5


def test_timer_prints_elapsed_time(capsys):
    @timer
    def wait():
        time.sleep(0.01)
    wait()
    output = capsys.readouterr().out
    assert "[timer]" in output
    assert "wait" in output


# ─────────────────────────────────────────────
# Tests for @retry
# ─────────────────────────────────────────────

def test_retry_runs_if_no_error():
    call_count = 0

    @retry(times=3)
    def stable_function():
        nonlocal call_count
        call_count += 1
        return "ok"

    result = stable_function()
    assert result == "ok"
    assert call_count == 1


def test_retry_retries_on_error():
    attempts = []

    @retry(times=3, exceptions=(ValueError,))
    def fails_twice():
        attempts.append(1)
        if len(attempts) < 3:
            raise ValueError("failure")
        return "success"

    result = fails_twice()
    assert result == "success"
    assert len(attempts) == 3


def test_retry_raises_after_all_attempts_exhausted():
    @retry(times=2, exceptions=(ValueError,))
    def always_fails():
        raise ValueError("always failing")

    with pytest.raises(ValueError):
        always_fails()


# ─────────────────────────────────────────────
# Tests for @memoize
# ─────────────────────────────────────────────

def test_memoize_returns_correct_result():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55


def test_memoize_caches_calls(capsys):
    fibonacci(5)
    fibonacci(5)
    output = capsys.readouterr().out
    assert "Cache hit" in output


# ─────────────────────────────────────────────
# Tests for calculate_sum (integration)
# ─────────────────────────────────────────────

def test_calculate_sum():
    assert calculate_sum(10) == 45
    assert calculate_sum(0) == 0
    assert calculate_sum(100) == 4950
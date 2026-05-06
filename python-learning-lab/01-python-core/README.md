# 01 · Python core

Practical exercises to master the parts of Python most used in real data and AI projects.

## Contents

| Folder | What you will learn |
|--------|---------------------|
| `decorators/` | Custom decorators, `functools`, `wraps`, decorators with parameters |
| `async_patterns/` | `asyncio`, `aiohttp`, real concurrency vs parallelism |
| `type_hints_pydantic/` | Type hints, Pydantic models, data validation, settings |
| `testing/` | `pytest`, fixtures, mocks, parametrize, coverage |

## Recommended order

1. `type_hints_pydantic/` — you will use this in every other module
2. `decorators/` — a fundamental pattern in libraries like FastAPI
3. `async_patterns/` — key for pipelines and API calls
4. `testing/` — write tests from the very beginning

## Running exercises

```bash
# Install dependencies
pip install -r requirements.txt

# Run an exercise
python decorators/01_basic_decorator.py

# Run tests
pytest tests/ -v
```
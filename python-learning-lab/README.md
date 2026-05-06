# python-learning-lab 🐍

A progressive learning project covering Python, AI, data engineering and DevOps.
Each module has practical exercises that feed into a **real integrator project**.

## Roadmap

| # | Module | Technologies | Status |
|---|--------|--------------|--------|
| 01 | [Python core](./01-python-core/) | decorators, async, Pydantic, pytest | 🚧 In progress |
| 02 | [Databases](./02-databases/) | PostgreSQL, MongoDB, Redis, SQLAlchemy | ⏳ Pending |
| 03 | [AI & Agents](./03-ai-agents/) | Anthropic/OpenAI SDK, RAG, embeddings | ⏳ Pending |
| 04 | [Data Engineering](./04-data-engineering/) | ETL, Pandas, Polars, Kafka | ⏳ Pending |
| 05 | [Containers & DevOps](./05-containers-devops/) | Docker, GitHub Actions, k8s | ⏳ Pending |
| 06 | [Integrator project](./06-integrator-project/) | Everything combined | ⏳ Pending |

## Integrator project

The end goal is a complete system that ties together everything learned:

```
┌──────────────────────────────────────────────┐
│              Integrator project              │
│                                              │
│  External data → ETL pipeline → PostgreSQL   │
│                              ↓               │
│                       FastAPI REST           │
│                              ↓               │
│                      AI Agent (RAG)          │
│                              ↓               │
│                  MongoDB (conversations)     │
└──────────────────────────────────────────────┘
```

## How to use this repo

1. Clone the repo and navigate to this directory
2. Start the databases from the integrator project:
   ```bash
   cd 06-integrator-project
   docker compose up -d
   ```
3. Follow the modules in order or jump to whichever interests you
4. Each folder has its own `README.md` with instructions

## General requirements

- Python 3.12+
- Docker + Docker Compose
- `uv` for environment management (recommended) or `pip`

## Repo conventions

- Each exercise has its own `README.md` explaining the goal
- Tests live in `tests/` inside each module
- Environment variables go in `.env` (never hardcoded)
- `.env.example` files show which variables are needed
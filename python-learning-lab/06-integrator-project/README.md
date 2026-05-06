# 06 · Integrator project

The project that ties together everything learned across the previous modules.
Built incrementally — starts simple and grows with each module completed.

## Target architecture

```
External data source (public API / CSV)
         │
         ▼
   ETL pipeline (Python)
         │
    ┌────┴────┐
    ▼         ▼
PostgreSQL  MongoDB
(clean       (logs,
 data)        conversations)
    │
    ▼
FastAPI REST
    │
    ▼
AI Agent (RAG over the data)
```

## Start the environment

```bash
# 1. Copy environment variables
cp .env.example .env
# Edit .env with your real values

# 2. Start databases
docker compose up -d

# 3. Check everything is healthy
docker compose ps

# 4. (Optional) Start admin UIs
docker compose --profile tools up -d
# pgAdmin       → http://localhost:5050
# Mongo Express → http://localhost:8081
```

## Available services

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 5432 | Relational database |
| MongoDB | 27017 | Document database |
| Redis | 6379 | Cache and pub/sub |
| pgAdmin | 5050 | PostgreSQL UI (profile: tools) |
| Mongo Express | 8081 | MongoDB UI (profile: tools) |

## Project phases

- [ ] **Phase 1** — ETL: ingest data from a public API into PostgreSQL
- [ ] **Phase 2** — REST API: expose the data with FastAPI
- [ ] **Phase 3** — AI Agent: add an agent that answers questions about the data
- [ ] **Phase 4** — Streaming: process events in real time with Redis pub/sub
- [ ] **Phase 5** — Observability: structured logs, metrics, traces

## Useful commands

```bash
# Stop everything
docker compose down

# Stop and delete volumes (resets databases)
docker compose down -v

# View logs for a service
docker compose logs postgres -f

# Connect directly to PostgreSQL
docker exec -it lab-postgres psql -U lab_user -d lab_db
```
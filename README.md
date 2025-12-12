Backend service built with Python (FastAPI) and Docker, with PostgreSQL + Alembic migrations, tests, and optional monitoring stack.

## Features
- REST API (FastAPI)
- PostgreSQL database
- Alembic migrations
- Docker + docker-compose for easy startup
- Pytest test suite
- Monitoring stack (Prometheus/Grafana) (optional)

## Tech Stack
- Python (Poetry)
- FastAPI
- PostgreSQL
- Alembic
- Docker / Docker Compose
- Pytest

1. quick install docker +docker compose 
2. create .env
3. start services
   docker compose up --build
4. open API docs
   Swagger UI: http://localhost:8000/docs
5. run migrations inside container
   docker compose exec fastapi alembic upgrade head





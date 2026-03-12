FastAPI Backend Service

Production-ready backend service built with Python and FastAPI, containerized with Docker and powered by PostgreSQL.
Includes database migrations, automated tests, and an optional monitoring stack.

This project demonstrates a modern backend architecture with containerized services, database versioning, and observability.

Features:

-RESTful API built with FastAPI
-PostgreSQL database integration
-Alembic database migrations
-Containerized deployment with Docker & Docker Compose
-Automated tests using Pytest
-Optional monitoring stack with Prometheus + Grafana
-Ready for local development and production deployment

Tech Stack:

-Python (managed with Poetry)
-FastAPI
-PostgreSQL
-SQLAlchemy
-Alembic
-Docker / Docker Compose
-Pytest
-Prometheus (optional)
-Grafana (optional)

Quick Start
1.Install Docker & Docker Compose

Install Docker from the official website and ensure Docker Compose is available.

2.Create environment file
Create a .env file in the project root.

Example:

POSTGRES_DB=app_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@db:5432/app_db

3.Start services

Run the following command:

      docker compose up --build

This will start:

--FastAPI application

--PostgreSQL database

--Optional monitoring services

4.Open API documentation

Swagger UI:

http://localhost:8000/docs

Alternative ReDoc interface:

http://localhost:8000/redoc

5.Run database migrations
Execute migrations inside the container:

      docker compose exec fastapi alembic upgrade head

Running Tests
Run the test suite with:

      docker compose exec fastapi pytest

Monitoring (Optional)
The monitoring stack includes:
Prometheus for metrics collection
Grafana for dashboards
Grafana dashboard:

http://localhost:3000

Project Structure

gpt_project
│
├── app
│   ├── api_router
│   ├── database
│   ├── generated_reports
│   ├── schemas
│   ├── services
│   ├── static
│   ├── tasks
│   ├── templates
│   ├── celery_app.py
│   └── config.py
│
├── migration
├── monitoring
├── tests
│
├── main.py
├── Dockerfile
├── pyproject.toml
├── alembic.ini
└── README.md

Author

Meerim Kadyrbekova
Python Backend Developer

GitHub: https://github.com/Mikulya3

LinkedIn: https://linkedin.com/in/meerim-kadyrbekova-770639b7





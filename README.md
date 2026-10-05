# Lemux — PropAnalyzer

## Intelligent Real-Estate Market Analysis Platform

Lemux is a full-stack real-estate analysis platform focused on collecting property-market data, processing it, and exposing analytical and price-prediction capabilities through a modular architecture.

The project is designed as a portfolio-grade example of **backend engineering + data processing + AI/ML + modern web development + containerized deployment**.

## Architecture

```text
                 ┌─────────────────────┐
                 │      Next.js        │
                 │      Frontend       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Django / DRF      │
                 │     Backend API     │
                 └──────┬──────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      PostgreSQL     Crawler       FastAPI
      / Data Store  / Processing   / AI & ML
                                      │
                                      ▼
                              Price Prediction
```

## Main Components

| Component | Responsibility |
|---|---|
| Django / DRF | Main backend and API layer |
| Next.js | Web application |
| Crawler | Market/property data collection |
| FastAPI | AI/ML service layer |
| PostgreSQL | Persistent data storage |
| Docker Compose | Multi-service development/deployment |
| Nginx | Reverse proxy |
| ML models | Property price analysis/prediction |

## Engineering Highlights

- Modular multi-service architecture
- Django REST API for the core backend
- Dedicated FastAPI service for AI/ML workloads
- Automated property-market data collection
- ML-based price prediction
- Dockerized backend, crawler, AI and frontend services
- Separate development and deployment Compose configurations
- Deployment and maintenance shell scripts
- Automated test/lint workflow documented in the project structure

## Project Structure

```text
Lemux/
├── backend/        # Django REST API
├── frontend/       # Next.js application
├── crawler/        # Data collection and processing
├── ai/             # FastAPI + ML services
├── docker/         # Compose, Nginx and monitoring
├── scripts/        # Setup, deploy, update and cleanup
└── .env.example    # Environment configuration template
```

## Running with Docker

From the repository root:

```bash
cd docker
docker-compose up --build
```

Typical local services:

- Frontend: `http://localhost:3000`
- Django backend: `http://localhost:8000`
- AI service: `http://localhost:8001`

For development:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

## Backend

The Django service contains the main API and database-facing application logic.

Typical development flow:

```bash
cd backend
python manage.py migrate
python manage.py test
```

## Deployment

The repository includes scripts for setup, deployment, data updates and cleanup.

```bash
./scripts/setup.sh
./scripts/deploy.sh
./scripts/update_data.sh
```

Use the project's `.env.example` as the starting point for environment configuration.

## Why This Project Matters

Lemux demonstrates the ability to work beyond a single Django application:

- designing service boundaries
- integrating AI/ML with a web backend
- handling data collection pipelines
- exposing APIs between services
- containerizing a multi-service system
- preparing a project for repeatable deployment

## Developer

**Nima Khadeh**

Backend-focused Software Developer  
Python · Django · DRF · PostgreSQL · Docker · AI/ML Integration


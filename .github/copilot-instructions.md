# Copilot Instructions

## Project Overview

This repository contains a **FastAPI backend** and a **React frontend**, each in their own folder:

- `backend/`: FastAPI application written in Python 3.13 using **Pydantic v2** for data validation and settings.
- `frontend/`: React application built with modern React (Hooks, functional components). Uses TypeScript if available.
- Both services are containerized and can be built and run using Dockerfile in each folder and a root-level `compose.yaml`.

## General Guidelines

- Always assume the project uses **Python 3.13** and **Pydantic v2**.
- Prefer **type hints**, **async/await**, and **dependency injection** with FastAPI.
- For Pydantic v2 models, use `model_validate`, `model_dump`, and `field_validator` instead of the v1 equivalents.
- When writing new API routes, include:
  - `@router.get/post/...` decorators.
  - Pydantic request/response models.
  - Proper error handling via `HTTPException`.
- Use **FastAPI dependency injection** for services, database sessions, and authentication.

## Backend Conventions

- Configuration is managed via Pydantic `BaseSettings` (v2) classes in a `config.py` file.
- Logging uses the standard `logging` module.
- Tests use `pytest` and can be found under `backend/tests`.

## Frontend Conventions

- Use modern React with functional components and hooks.
- For API calls, use a central `api.ts` file or React Query hooks that call the FastAPI backend.
- Use environment variables (e.g. `VITE_API_URL` or `REACT_APP_API_URL`) for backend endpoints.
- Use TypeScript interfaces that mirror the Pydantic models in the backend.

## Containerization

- Both backend and frontend have their own Dockerfiles.
- A root-level `compose.yaml` orchestrates containers.
- Backend listens on port 8000, frontend on 3000 (unless otherwise specified).

## Code Style

- **Python**: Follow PEP 8, use `ruff` for formatting and linting.
- **JavaScript/TypeScript**: Follow ESLint + Prettier rules.
- Include docstrings for public functions and classes.
- Use descriptive variable and function names.

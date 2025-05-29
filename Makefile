# Project Makefile for Async FastAPI Task API

.PHONY: help install run dev test lint fmt migrate upgrade makemigrations resetdb docker-up docker-down

SRC_DIRS = app tests

# --------------------
# General Commands
# --------------------

help:
	@echo "Usage:"
	@echo "  make install          Install dependencies using Poetry"
	@echo "  make run              Run FastAPI app with Uvicorn"
	@echo "  make dev              Run app with live reload"
	@echo "  make test             Run all unit tests"
	@echo "  make lint             Run linter (ruff)"
	@echo "  make fmt              Format code (black + ruff --fix)"
	@echo "  make migrate          Create new Alembic migration"
	@echo "  make upgrade          Apply Alembic migrations"
	@echo "  make resetdb          Drop and recreate all tables"
	@echo "  make docker-up        Start PostgreSQL with Docker"
	@echo "  make docker-down      Stop and remove Docker containers"

# --------------------
# Dev / App
# --------------------

install:
	poetry install

run:
	poetry run uvicorn app.entrypoints.fastapi_app:app --host 0.0.0.0 --port 8000

dev:
	poetry run uvicorn app.entrypoints.fastapi_app:app --reload

test:
	poetry run alembic upgrade head
	poetry run pytest -vv

lint:
	poetry run ruff check $(SRC_DIRS)

fmt:
	poetry run black $(SRC_DIRS)
	poetry run isort $(SRC_DIRS)
	poetry run ruff check $(SRC_DIRS) --fix

# --------------------
# Database / Alembic
# --------------------

migrate:
	poetry run alembic revision --autogenerate -m "migration"

upgrade:
	poetry run alembic upgrade head

resetdb:
	poetry run alembic downgrade base
	poetry run alembic upgrade head

# --------------------
# Docker (for PostgreSQL)
# --------------------

docker-up:
	docker compose up -d

docker-down:
	docker compose down
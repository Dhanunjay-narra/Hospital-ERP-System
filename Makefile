# ApexCare Hospital ERP + CRM Master Automation Makefile
.PHONY: help install build test run dev docker-up docker-down clean migrate seed

help:
	@echo "ApexCare Hospital ERP + CRM Build System"
	@echo "Available commands:"
	@echo "  make install     - Install backend and frontend dependencies"
	@echo "  make build       - Build production Next.js frontend"
	@echo "  make test        - Run complete 33-module Pytest test suite"
	@echo "  make run         - Run production FastAPI server"
	@echo "  make dev         - Run development servers"
	@echo "  make docker-up   - Launch multi-container Docker stack"
	@echo "  make docker-down - Terminate Docker stack"
	@echo "  make seed        - Initialize and seed master data"

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

build:
	cd frontend && npm run build

test:
	cd backend && pytest -v

run:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	cd backend && uvicorn app.main:app --reload --port 8000 &
	cd frontend && npm run dev

seed:
	cd backend && python -m app.seed.seed_data

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

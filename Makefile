# ==========================================
# Mark: Dev
# ==========================================
start_dev:
	docker compose -f docker-compose.dev.yml up -d --build

stop_dev:
	docker compose -f docker-compose.dev.yml down

remove_dev:
	docker compose -f docker-compose.dev.yml down -v

logs_backend:
	docker logs -f backend-notes-dev

logs_frontend:
	docker logs -f frontend-notes-dev

# ==========================================
# Mark: Prod
# ==========================================


# ==========================================
# Mark: Lint And Tests
# ==========================================

backend_lint:
	cd backend && uv run ruff check src

backend_mypy:
	cd backend && uv run mypy src

backend_test:
	cd backend && uv run pytest || [ $$? -eq 5 ]

backend_ci: backend_lint backend_test backend_mypy

backend_coverage_html:
	cd backend && uv run pytest tests --cov=src --cov-report=html

backend_coverage:
	cd backend && uv run pytest tests --cov=src --cov-report=term-missing

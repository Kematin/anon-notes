# ==========================================
# Mark: Dev
# ==========================================
start_dev:
	docker compose -f docker-compose.dev.yml up -d --build

stop_dev:
	docker compose -f docker-compose.dev.yml down

remove_dev:
	docker compose -f docker-compose.dev.yml down -v

logs_backend_dev:
	docker logs -f backend-notes-dev

logs_frontend_dev:
	docker logs -f frontend-notes-dev

# ==========================================
# Mark: Prod
# ==========================================
start_prod:
	docker compose -f docker-compose.prod.yml up -d --build

stop_prod:
	docker compose -f docker-compose.prod.yml down

remove_prod:
	docker compose -f docker-compose.prod.yml down -v

logs_backend:
	docker logs -f backend-notes-prod

logs_nginx:
	docker logs -f nginx-notes-prod

# ==========================================
# Mark: Backend Lint And Tests
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

# ==========================================
# Mark: Frontend Lint And Tests
# ==========================================

FRONTEND_DIR = frontend/app

front_types:
	cd $(FRONTEND_DIR) && npx tsc --noEmit

front_lint:
	cd $(FRONTEND_DIR) && npm run lint

front_build:
	cd $(FRONTEND_DIR) && npm run build

front_ci: front-types front-lint front-build

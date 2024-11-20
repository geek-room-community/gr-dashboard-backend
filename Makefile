# Variables
FLASK_APP=app.py
FLASK_ENV=development


.PHONY: run
run:
	@echo "Starting the Flask application..."
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run

.PHONY: init-db
init-db:
	@echo "Initializing the database..."
	python3 -c 'from app import db, app; from models import User; with app.app_context(): db.create_all()'


.PHONY: install
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt


.PHONY: env
env:
	@echo "Creating .env file if it doesn't exist..."
	@if [ ! -f .env ]; then echo "DATABASE_URL=postgresql://username:password@localhost:5432/your_database" > .env; fi

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	pytest

.PHONY: migrate
migrate:
	@echo "Applying database migrations..."
	flask db migrate -m "Migration"
	flask db upgrade

.PHONY: clean
clean:
	@echo "Cleaning up..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete


.PHONY: lint
lint:
	@echo "Linting code with flake8..."
	flake8 .


.PHONY: reset-db
reset-db:
	@echo "Resetting the database..."
	python3 -c 'from app import db, app; with app.app_context(): db.drop_all(); db.create_all()'

.PHONY: dev
dev:
	@echo "Starting Flask in development mode with hot reload..."
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run --reload

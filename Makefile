.PHONY: run test install install-dev show-structure help

help:
	@echo "Available targets:"
	@echo "  install        : Install dependencies for production"
	@echo "  install-dev    : Install dependencies for development"
	@echo "  run            : Run project"
	@echo "  test           : Run test suite"
	@echo "  format         : Format code"
	@echo "  tree           : Show project directory structure as tree"
	@echo "  help           : Display this help message"

install:
	poetry install --without dev

install-dev:
	poetry install && poetry run pre-commit install

run:
	poetry run python src/main.py

test:
	poetry run pytest .

format:
	poetry run pre-commit run --all-files

tree:
	tree -a -I '__pycache__|*.pyc|*.pyo|.pytest_cache|.venv|.git|.idea'

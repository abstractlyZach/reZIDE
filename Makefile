all: format test lint typecheck

test: poetry.lock
	poetry run pytest --cov -m "not e2e"

format: poetry.lock
	# reformat all files
	poetry run black .
	poetry run isort .

lint: poetry.lock
	poetry run flake8

typecheck: poetry.lock
	# install type stubs for 3rd party libraries if they're missing but
	#   available for installation
	# https://mypy.readthedocs.io/en/stable/running_mypy.html#library-stubs-not-installed
	poetry run mypy --install-types --non-interactive .

# install the project whenever the pyproject.toml file changes,
# using poetry.lock as an indicator of the last time we updated it
poetry.lock: pyproject.toml
	poetry install
	# update the modification time in case the file doesn't get updated
	touch poetry.lock

dev-setup: ci-setup
	pre-commit install

ci-setup:
	poetry install

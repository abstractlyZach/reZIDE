all: format test lint typecheck

test:
	poetry run pytest --cov -m "not e2e"

format:
	# reformat all files
	poetry run black .
	poetry run isort .

lint:
	poetry run flake8

typecheck:
	# install type stubs for 3rd party libraries if they're missing but
	#   available for installation
	# https://mypy.readthedocs.io/en/stable/running_mypy.html#library-stubs-not-installed
	poetry run mypy --install-types --non-interactive .

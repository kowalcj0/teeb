
.PHONY: tests
tests:
	pytest tests

.PHONY: clean
clean:
	-rm -fr .cache/
	-rm -fr .pytest_cache/
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete
	-find . -type f -name "*.log" -delete

.PHONY: lint
lint:
	flake8
	pylint
	mypy

.PHONY: format
format:
	isort **/*.py
	black

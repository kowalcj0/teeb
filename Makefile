
.PHONY: tests
tests:
	pytest --cov --cov-append tests

.PHONY: clean
clean:
	-rm -fr .coverage*
	-rm -fr .cache/
	-rm -fr .pytest_cache/
	-find . -type d -name "*egg-info" -exec rm -rf {} +
	-find . -type d -name "__pycache__" -exec rm -rf {} +
	-find . -type f -name "*.pyc" -delete
	-find . -type f -name "*.log" -delete

.PHONY: lint
lint:
	@echo "===================== Flake8"
	-flake8
	@echo "===================== PyLint"
	-pylint **/*.py
	@echo "===================== Mypy"
	mypy **/*.py

.PHONY: format
format:
	isort .
	black .

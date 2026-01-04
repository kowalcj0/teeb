
.PHONY: tests
tests:
	uv run pytest --cov --cov-append src/tests

.PHONY: clean
clean:
	-rm -fr .coverage*
	-rm -fr .cache/
	-rm -fr .pytest_cache/
	-find . -type d -name "*egg-info" -exec rm -rf {} +
	-find . -type d -name "__pycache__" -exec rm -rf {} +
	-find . -type f -name "*.pyc" -delete
	-find . -type f -name "*.log" -delete

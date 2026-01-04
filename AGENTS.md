# Agent Guidelines for Teeb

## Build/Test Commands
- Run all tests: `make tests` or `pytest --cov --cov-append tests`
- Run single test: `pytest tests/unit/test_find.py::test_find_extra_files`
- Run specific test file: `pytest tests/unit/test_find.py`
- Lint: `make lint` (uses flake8, pylint, mypy - note: Makefile may be outdated, prefer ruff)
- Format: `ruff format .` or `ruff check --fix .`
- Clean build artifacts: `make clean`

## Code Style
- **Python version**: 3.13+ required
- **Formatter**: Ruff (pre-commit hook configured)
- **Line length**: 88 characters (Black-compatible)
- **Imports**: Use absolute imports from `teeb.*` modules; group by stdlib, third-party, local
- **Type hints**: Use type hints for function signatures (see `find.py` examples)
- **Docstrings**: Use for public functions, include purpose and examples where helpful
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Error handling**: Use try/except with specific exceptions; print user-friendly messages
- **String quotes**: Double quotes preferred, double for docstrings

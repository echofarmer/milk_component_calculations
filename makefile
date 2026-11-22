# CMSE Project Commands
#
# Run:
#     make help
#
# after activating your environment.

PACKAGE = milk_component_calculations

help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make init       Create/update milk_component_calculations conda environment"
	@echo "  make run        Run the full workflow on the example data"
	@echo "  make lint       Check code with Ruff"
	@echo "  make format     Format code with Ruff"
	@echo "  make test       Run tests"
	@echo "  make type       Run MyPy"
	@echo "  make docs       Build documentation"
	@echo "  make check      Run lint and tests"
	@echo "  make clean      Remove generated files"
	@echo ""

init:
	conda env create -f environment.yml || conda env update -f environment.yml --prune

run:
	python -m $(PACKAGE).pipeline

lint:
	ruff check .

format:
	ruff format .

test:
	pytest -v

type:
	mypy $(PACKAGE)

# Python deletes the folders so these commands also work on Windows
docs:
	python -c "import shutil; shutil.rmtree('docs', ignore_errors=True)"
	pdoc -o docs $(PACKAGE)

check: lint test

check-full: lint type test

clean:
	python -c "import shutil; shutil.rmtree('docs', ignore_errors=True)"
	python -c "import shutil; shutil.rmtree('outputs', ignore_errors=True)"
	python -c "import shutil; shutil.rmtree('.pytest_cache', ignore_errors=True)"
	python -c "import shutil; shutil.rmtree('.mypy_cache', ignore_errors=True)"
	python -c "import shutil; shutil.rmtree('.ruff_cache', ignore_errors=True)"

.PHONY: help init run lint format test type docs check check-full clean

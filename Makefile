.PHONY: help azure-ready install test lint clean

help:
	@echo "Q-LOCK Attractor Engine - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make azure-ready   - Setup for Azure ML environment"
	@echo "  make install       - Install dependencies locally"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make clean         - Clean up temporary files"

azure-ready:
	@echo "Setting up Q-LOCK for Azure ML..."
	@bash scripts/azure_setup.sh
	@echo ""
	@echo "Azure ML setup complete!"

install:
	@echo "Installing Q-LOCK dependencies..."
	pip install -e .
	@echo "Installation complete!"

test:
	@echo "Running tests..."
	pytest tests/ -v

lint:
	@echo "Running flake8..."
	flake8 q_lock_cli.py q_lock_engine.py Src/

clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	rm -rf output/
	rm -rf runs/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"

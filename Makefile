# define the name of the virtual environment directory
VENV := venv

# Variables
PIP := $(VENV)/bin/pip
PYTHON := $(VENV)/bin/python
REQUIREMENTS := requirements.txt

# Default target, when make executed without arguments
all: help

# Help menu
help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  venv          - Create a virtual environment"
	@echo "  activate      - Activating environment"
	@echo "  install       - Install dependencies"
	@echo "  lint          - Run pylint linter"
	@echo "  format        - Run code formatter using black"
	@echo "  test          - Run tests and coverage using pytest"
	@echo "  clean         - Clean up unnecessary files"
	@echo "  clean-venv    - Remove virtual environment"

# Create a virtual environment
venv:
	@echo "Creating virtual environment..."
	@/bin/bash -c "python3.9 -m venv $(VENV)"
	@echo "Virtual environment created."

# Activate environment
activate: venv
	@echo "Activating environment..."
	@/bin/bash -c "source $(VENV)/bin/activate" 
	@echo "Environment activated"

# Install dependencies
install: activate
	@echo "Installing dependencies..."
	@/bin/bash -c "pip install --upgrade pip"
	@/bin/bash -c "pip install -r $(REQUIREMENTS)"
	@echo "Dependencies installed"

# Run tests and coverage using pytest
test: install
	@echo "Running tests and coverage..."
	@/bin/bash -c "coverage run -m pytest -v"
	@/bin/bash -c "coverage report -m"

# Run code formatter using black
format: install
	@echo "Running formatter..."
	@/bin/bash -c "black ."
	@echo "Code formatted"

# Run linter using pylint
lint: install
	@echo "Running linter..."
	@/bin/bash -c "pylint --recursive=y ."

# # Clean up unnecessary files
# .PHONY: clean
# clean:
# 	@echo "Cleaning up..."
# 	find . -type f -name "*.pyc" -delete
# 	find . -type d -name "__pycache__" -exec rm -rf {} +

# # Remove virtual environment
# .PHONY: clean-venv
# clean-venv:
# 	@echo "Removing virtual environment..."
# 	rm -rf $(VENV_DIR)

.PHONY: all help venv activate install format lint test

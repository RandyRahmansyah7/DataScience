# ==============================================================================
# Makefile for Retail Profitability Analyzer
# ==============================================================================

.PHONY: help venv install run clean

# -- Variables --
APP_FILE = app.py
REQ_FILE = requirements.txt
VENV_DIR = venv

# -- Targets --

help:
	@echo "Retail Profitability Analyzer - Available commands:"
	@echo ""
	@echo "  make venv      - Create a Python virtual environment"
	@echo "  make install   - Install dependencies from $(REQ_FILE)"
	@echo "  make run       - Run the Streamlit dashboard"
	@echo "  make clean     - Remove Python cache files (.pyc, __pycache__)"
	@echo ""

venv:
	@echo "Creating virtual environment in '$(VENV_DIR)'..."
	python3 -m venv $(VENV_DIR)
	@echo "Done! Activate it using: source $(VENV_DIR)/bin/activate (Linux/Mac) or $(VENV_DIR)\Scripts\activate (Windows)"

install:
	@echo "Installing dependencies..."
	pip install -r $(REQ_FILE)

run:
	@echo "Starting the Streamlit app..."
	streamlit run $(APP_FILE)

clean:
	@echo "Cleaning up cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "Clean up complete."
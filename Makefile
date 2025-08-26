# Makefile for MainzDigitizer (CAEN Parser)
# Automatiza la limpieza, construcción e instalación del proyecto

# Variables
PYTHON := python3
PIP := pip
PROJECT_DIR := $(shell pwd)
SRC_DIR := src
BUILD_DIR := build
EGG_INFO := src/caenParser.egg-info

# Output colors
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

# Default target
.PHONY: help
help:
	@echo "$(BLUE)MainzDigitizer - CAEN Parser Makefile$(RESET)"
	@echo ""
	@echo "$(YELLOW)Available targets:$(RESET)"
	@echo "  $(GREEN)install$(RESET)          - Installs the package in development mode"
	@echo "  $(GREEN)clean$(RESET)            - Cleans build and cache files"
	@echo "  $(GREEN)clean-all$(RESET)        - Full cleanup + duplicate files"
	@echo "  $(GREEN)build$(RESET)            - Builds the package (without installing)"
	@echo "  $(GREEN)rebuild$(RESET)          - Cleans and reinstalls from scratch"
	@echo "  $(GREEN)test$(RESET)             - Runs tests"
	@echo "  $(GREEN)check-env$(RESET)        - Checks development environment"
	@echo "  $(GREEN)dev-setup$(RESET)        - Initial setup for development"
	@echo "  $(GREEN)uninstall$(RESET)        - Uninstalls the package"
	@echo "  $(GREEN)show-structure$(RESET)   - Shows project structure"
	@echo ""

# Development mode installation
.PHONY: install
install: check-env
	@echo "$(BLUE)Installing caenParser in development mode...$(RESET)"
	$(PIP) install -e .
	@echo "$(GREEN)✓ Installation completed$(RESET)"

# Basic cleanup
.PHONY: clean
clean:
	@echo "$(YELLOW)Cleaning build and cache files...$(RESET)"
	@rm -rf $(BUILD_DIR)/
	@rm -rf $(EGG_INFO)/
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.so" -delete
	@echo "$(GREEN)✓ Basic cleanup completed$(RESET)"

# Full cleanup
.PHONY: clean-all
clean-all: clean
	@echo "$(YELLOW)Performing full cleanup...$(RESET)"
	@# Remove duplicate files outside src/caenParser/
	@rm -rf src/domain/ 2>/dev/null || true
	@rm -rf src/persistence/ 2>/dev/null || true
	@rm -f __init__.py __main__.py 2>/dev/null || true
	@# Remove optional directories
	@rm -rf .DATA/ 2>/dev/null || true
	@rm -rf .vscode/ 2>/dev/null || true
	@rm -rf tests/.TEST_DATA/ 2>/dev/null || true
	@# Remove temporary compiler files
	@find . -name "*.o" -delete 2>/dev/null || true
	@find . -name "*.obj" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Full cleanup finished$(RESET)"

# Build only (no install)
.PHONY: build
build: check-env
	@echo "$(BLUE)Building the package...$(RESET)"
	$(PYTHON) setup.py build_ext --inplace
	@echo "$(GREEN)✓ Build completed$(RESET)"

# Full rebuild
.PHONY: rebuild
rebuild: clean-all install
	@echo "$(GREEN)✓ Rebuild completed$(RESET)"

# Run tests
.PHONY: test
test:
	@echo "$(BLUE)Running tests...$(RESET)"
	@if [ -f pytest.ini ]; then \
		$(PYTHON) -m pytest -v; \
	else \
		$(PYTHON) -m pytest tests/ -v; \
	fi
	@echo "$(GREEN)✓ Tests completed$(RESET)"

# Check environment
.PHONY: check-env
check-env:
	@echo "$(BLUE)Checking development environment...$(RESET)"
	@$(PYTHON) --version || (echo "$(RED)✗ Python not found$(RESET)" && exit 1)
	@$(PIP) --version || (echo "$(RED)✗ pip not found$(RESET)" && exit 1)
	@$(PYTHON) -c "import pybind11" 2>/dev/null || (echo "$(RED)✗ pybind11 not found. Install with: pip install pybind11$(RESET)" && exit 1)
	@echo "$(GREEN)✓ Environment checked$(RESET)"

# Initial setup for development
.PHONY: dev-setup
dev-setup:
	@echo "$(BLUE)Setting up development environment...$(RESET)"
	@$(PIP) install --upgrade pip
	@$(PIP) install pybind11 pytest pandas
	@echo "$(GREEN)✓ Environment setup completed$(RESET)"

# Uninstall package
.PHONY: uninstall
uninstall:
	@echo "$(YELLOW)Uninstalling caenParser...$(RESET)"
	@$(PIP) uninstall caenParser -y 2>/dev/null || echo "$(YELLOW)Package was not installed$(RESET)"
	@echo "$(GREEN)✓ Uninstallation completed$(RESET)"

# Show project structure
.PHONY: show-structure
show-structure:
	@echo "$(BLUE)Project structure:$(RESET)"
	@tree -I '__pycache__|*.pyc|*.so|build|*.egg-info' . 2>/dev/null || \
	find . -type f ! -path './__pycache__/*' ! -name '*.pyc' ! -name '*.so' ! -path './build/*' ! -path './*.egg-info/*' | sort

# Check C++ syntax errors
.PHONY: check-cpp
check-cpp:
	@echo "$(BLUE)Checking C++ file syntax...$(RESET)"
	@for file in src/cpp/*.cpp src/cpp/*.h; do \
		if [ -f "$$file" ]; then \
			echo "Checking $$file..."; \
			g++ -fsyntax-only -std=c++11 -I./src/cpp/ $$file 2>/dev/null || \
			echo "$(RED)✗ Syntax error in $$file$(RESET)"; \
		fi \
	done
	@echo "$(GREEN)✓ C++ check completed$(RESET)"

# Fast development install (cleans only necessary and reinstalls)
.PHONY: dev-install
dev-install: clean install
	@echo "$(GREEN)✓ Development install completed$(RESET)"

# Show installed package info
.PHONY: info
info:
	@echo "$(BLUE)Installed package info:$(RESET)"
	@$(PIP) show caenParser 2>/dev/null || echo "$(YELLOW)Package not installed$(RESET)"

# CI/CD target
.PHONY: ci
ci: check-env clean-all build test
	@echo "$(GREEN)✓ CI pipeline completed$(RESET)"

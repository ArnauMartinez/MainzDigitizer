# Makefile for MainzDigitizer (CAEN Parser)
# Automatiza la limpieza, construcción e instalación del proyecto

# Variables
PYTHON := python3
PIP := pip
PROJECT_DIR := $(shell pwd)
SRC_DIR := src
BUILD_DIR := build
EGG_INFO := src/caenParser.egg-info

# Colores para output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

# Target por defecto
.PHONY: help
help:
	@echo "$(BLUE)MainzDigitizer - CAEN Parser Makefile$(RESET)"
	@echo ""
	@echo "$(YELLOW)Targets disponibles:$(RESET)"
	@echo "  $(GREEN)install$(RESET)          - Instala el paquete en modo desarrollo"
	@echo "  $(GREEN)clean$(RESET)            - Limpia archivos de build y cache"
	@echo "  $(GREEN)clean-all$(RESET)        - Limpieza completa + archivos duplicados"
	@echo "  $(GREEN)build$(RESET)            - Construye el paquete (sin instalar)"
	@echo "  $(GREEN)rebuild$(RESET)          - Limpia y reinstala desde cero"
	@echo "  $(GREEN)test$(RESET)             - Ejecuta los tests"
	@echo "  $(GREEN)check-env$(RESET)        - Verifica el entorno de desarrollo"
	@echo "  $(GREEN)dev-setup$(RESET)        - Configuración inicial para desarrollo"
	@echo "  $(GREEN)uninstall$(RESET)        - Desinstala el paquete"
	@echo "  $(GREEN)show-structure$(RESET)   - Muestra la estructura del proyecto"
	@echo ""

# Instalación en modo desarrollo
.PHONY: install
install: check-env
	@echo "$(BLUE)Instalando caenParser en modo desarrollo...$(RESET)"
	$(PIP) install -e .
	@echo "$(GREEN)✓ Instalación completada$(RESET)"

# Limpieza básica
.PHONY: clean
clean:
	@echo "$(YELLOW)Limpiando archivos de build y cache...$(RESET)"
	@rm -rf $(BUILD_DIR)/
	@rm -rf $(EGG_INFO)/
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.so" -delete
	@echo "$(GREEN)✓ Limpieza básica completada$(RESET)"

# Limpieza completa
.PHONY: clean-all
clean-all: clean
	@echo "$(YELLOW)Realizando limpieza completa...$(RESET)"
	@# Eliminar archivos duplicados fuera de src/caenParser/
	@rm -rf src/domain/ 2>/dev/null || true
	@rm -rf src/persistence/ 2>/dev/null || true
	@rm -f __init__.py __main__.py 2>/dev/null || true
	@# Eliminar directorios opcionales
	@rm -rf .DATA/ 2>/dev/null || true
	@rm -rf .vscode/ 2>/dev/null || true
	@rm -rf tests/.TEST_DATA/ 2>/dev/null || true
	@# Eliminar archivos temporales del compilador
	@find . -name "*.o" -delete 2>/dev/null || true
	@find . -name "*.obj" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Limpieza completa terminada$(RESET)"

# Solo construcción (sin instalación)
.PHONY: build
build: check-env
	@echo "$(BLUE)Construyendo el paquete...$(RESET)"
	$(PYTHON) setup.py build_ext --inplace
	@echo "$(GREEN)✓ Construcción completada$(RESET)"

# Reconstrucción completa
.PHONY: rebuild
rebuild: clean-all install
	@echo "$(GREEN)✓ Reconstrucción completada$(RESET)"

# Ejecutar tests
.PHONY: test
test:
	@echo "$(BLUE)Ejecutando tests...$(RESET)"
	@if [ -f pytest.ini ]; then \
		$(PYTHON) -m pytest -v; \
	else \
		$(PYTHON) -m pytest tests/ -v; \
	fi
	@echo "$(GREEN)✓ Tests completados$(RESET)"

# Verificar entorno
.PHONY: check-env
check-env:
	@echo "$(BLUE)Verificando entorno de desarrollo...$(RESET)"
	@$(PYTHON) --version || (echo "$(RED)✗ Python no encontrado$(RESET)" && exit 1)
	@$(PIP) --version || (echo "$(RED)✗ pip no encontrado$(RESET)" && exit 1)
	@$(PYTHON) -c "import pybind11" 2>/dev/null || (echo "$(RED)✗ pybind11 no encontrado. Instala con: pip install pybind11$(RESET)" && exit 1)
	@echo "$(GREEN)✓ Entorno verificado$(RESET)"

# Configuración inicial para desarrollo
.PHONY: dev-setup
dev-setup:
	@echo "$(BLUE)Configurando entorno de desarrollo...$(RESET)"
	@$(PIP) install --upgrade pip
	@$(PIP) install pybind11 pytest pandas
	@echo "$(GREEN)✓ Entorno configurado$(RESET)"

# Desinstalar paquete
.PHONY: uninstall
uninstall:
	@echo "$(YELLOW)Desinstalando caenParser...$(RESET)"
	@$(PIP) uninstall caenParser -y 2>/dev/null || echo "$(YELLOW)Paquete no estaba instalado$(RESET)"
	@echo "$(GREEN)✓ Desinstalación completada$(RESET)"

# Mostrar estructura del proyecto
.PHONY: show-structure
show-structure:
	@echo "$(BLUE)Estructura del proyecto:$(RESET)"
	@tree -I '__pycache__|*.pyc|*.so|build|*.egg-info' . 2>/dev/null || \
	find . -type f ! -path './__pycache__/*' ! -name '*.pyc' ! -name '*.so' ! -path './build/*' ! -path './*.egg-info/*' | sort

# Verificar errores de sintaxis en código C++
.PHONY: check-cpp
check-cpp:
	@echo "$(BLUE)Verificando sintaxis de archivos C++...$(RESET)"
	@for file in src/cpp/*.cpp src/cpp/*.h; do \
		if [ -f "$$file" ]; then \
			echo "Verificando $$file..."; \
			g++ -fsyntax-only -std=c++11 -I./src/cpp/ $$file 2>/dev/null || \
			echo "$(RED)✗ Error de sintaxis en $$file$(RESET)"; \
		fi \
	done
	@echo "$(GREEN)✓ Verificación C++ completada$(RESET)"

# Target para desarrollo rápido (limpia solo lo necesario y reinstala)
.PHONY: dev-install
dev-install: clean install
	@echo "$(GREEN)✓ Instalación de desarrollo completada$(RESET)"

# Mostrar información del paquete instalado
.PHONY: info
info:
	@echo "$(BLUE)Información del paquete instalado:$(RESET)"
	@$(PIP) show caenParser 2>/dev/null || echo "$(YELLOW)Paquete no instalado$(RESET)"

# Target para CI/CD
.PHONY: ci
ci: check-env clean-all build test
	@echo "$(GREEN)✓ Pipeline CI completado$(RESET)"

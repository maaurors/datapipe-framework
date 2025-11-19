.PHONY: help setup build-generators init test-framework clean

help:
	@echo ""
	@echo "DataPipe Framework - Comandos:"
	@echo ""
	@echo "  setup              - Instalar dependencias"
	@echo "  build-generators   - Construir generadores Docker"
	@echo "  init               - Crear nuevo proyecto"
	@echo "  test-framework     - Probar framework"
	@echo "  clean              - Limpiar cache"
	@echo ""

setup:
	@echo "Instalando dependencias..."
	pip3 install cookiecutter pyyaml
	@echo "Setup completado"

build-generators:
	@echo "Construyendo generadores..."
	@echo "Building schema-generator..."
	cd generators/schema-generator && docker build -t datapipe/schema-generator:latest .
	@echo "Building table-generator..."
	cd generators/table-generator && docker build -t datapipe/table-generator:latest .
	@echo "Building procedure-generator..."
	cd generators/procedure-generator && docker build -t datapipe/procedure-generator:latest .
	@echo "Building dag-generator..."
	cd generators/dag-generator && docker build -t datapipe/dag-generator:latest .
	@echo "Generadores construidos"
	@docker images | grep datapipe

init:
	@echo "Creando nuevo proyecto..."
	cookiecutter generators/cookiecutter-datapipe/
	@echo "Proyecto creado"

test-framework:
	@echo "Testing framework..."
	docker run --rm datapipe/schema-generator:latest python --version
	@echo "Framework OK"

clean:
	@echo "Limpiando..."
	docker system prune -f
	@echo "Limpieza completada"

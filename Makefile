.PHONY: help init-cloud build-cloud build-generators build-components test-all test-manual clean

help:
	@echo "DataPipe Framework - Comandos Multi-Cloud"
	@echo ""
	@echo "  make init-cloud CLOUD=gcp TABLE_NAME=mi_tabla LOAD_MODE=incremental"
	@echo "  make build-cloud CLOUD=gcp"
	@echo "  make build-generators"
	@echo "  make build-components CLOUD=gcp"
	@echo "  make test-all TABLE_NAME=test_table"
	@echo "  make test-manual TABLE_NAME=test_table"
	@echo "  make clean"
	@echo ""

init-cloud:
ifndef CLOUD
	$(error CLOUD no definido. Uso: make init-cloud CLOUD=gcp|aws|azure TABLE_NAME=xxx LOAD_MODE=full|incremental)
endif
	@echo "Inicializando proyecto:"
	@echo "   Cloud: $(CLOUD)"
	@echo "   Tabla: $(TABLE_NAME)"
	@echo "   Modo: $(LOAD_MODE)"
	@mkdir -p clouds/$(CLOUD)/{extractor,loader,transformer}/src
	@mkdir -p templates/$(CLOUD)/{{cookiecutter.project_slug}}
	@mkdir -p projects/$(CLOUD)_$(TABLE_NAME)
	@mkdir -p output
	@echo "Estructura creada para $(TABLE_NAME) en $(CLOUD)"

build-cloud:
ifndef CLOUD
	$(error CLOUD no definido. Uso: make build-cloud CLOUD=gcp|aws|azure)
endif
	@echo "Construyendo imagenes para: $(CLOUD)"
	@docker build -t datapipe/schema-generator:latest generators/schema-generator/
	@docker build -t datapipe/table-generator:latest generators/table-generator/
	@docker build -t datapipe/procedure-generator:latest generators/procedure-generator/
	@docker build -t datapipe/dag-generator:latest generators/dag-generator/
	@echo "Generadores construidos para $(CLOUD)"

build-generators:
	@echo "Construyendo todos los generadores..."
	cd generators/schema-generator && docker build -t datapipe/schema-generator:latest .
	cd generators/table-generator && docker build -t datapipe/table-generator:latest .
	cd generators/procedure-generator && docker build -t datapipe/procedure-generator:latest .
	cd generators/dag-generator && docker build -t datapipe/dag-generator:latest .
	@echo "Todos los generadores construidos"

build-components:
ifndef CLOUD
	$(error CLOUD no definido. Uso: make build-components CLOUD=gcp|aws|azure)
endif
	@echo "Construyendo componentes para: $(CLOUD)"
	@docker build -t datapipe/extractor-$(CLOUD):latest clouds/$(CLOUD)/extractor/ 2>/dev/null || echo "Extractor no configurado para $(CLOUD)"
	@docker build -t datapipe/loader-$(CLOUD):latest clouds/$(CLOUD)/loader/ 2>/dev/null || echo "Loader no configurado para $(CLOUD)"
	@docker build -t datapipe/transformer-$(CLOUD):latest clouds/$(CLOUD)/transformer/ 2>/dev/null || echo "Transformer no configurado para $(CLOUD)"
	@echo "Componentes construidos para $(CLOUD)"

test-all:
ifndef TABLE_NAME
	$(error TABLE_NAME no definido. Uso: make test-all TABLE_NAME=test_table)
endif
	@echo "Probando todos los generadores con tabla: $(TABLE_NAME)"
	@mkdir -p output
	@echo "Probando Schema Generator..."
	@docker run --rm -v $(PWD)/output:/output datapipe/schema-generator:latest --table-name=$(TABLE_NAME) --cloud=gcp || echo "Schema Generator fallo"
	@echo "Probando Table Generator..."
	@docker run --rm datapipe/table-generator:latest --table-name=$(TABLE_NAME) --cloud=gcp || echo "Table Generator fallo"
	@echo "Probando Procedure Generator..."
	@docker run --rm datapipe/procedure-generator:latest --table-name=$(TABLE_NAME) --cloud=gcp --load-mode=incremental || echo "Procedure Generator fallo"
	@echo "Probando DAG Generator..."
	@docker run --rm datapipe/dag-generator:latest --table-name=$(TABLE_NAME) --cloud=gcp --load-mode=incremental || echo "DAG Generator fallo"
	@echo "Pruebas completadas"

test-manual:
ifndef TABLE_NAME
	$(error TABLE_NAME no definido. Uso: make test-manual TABLE_NAME=test_table)
endif
	@echo "Prueba manual paso a paso:"
	@mkdir -p output
	@echo "1. Schema Generator:"
	docker run --rm -v $(PWD)/output:/output datapipe/schema-generator:latest --table-name=$(TABLE_NAME) --cloud=gcp
	@echo "2. Table Generator:"
	docker run --rm datapipe/table-generator:latest --table-name=$(TABLE_NAME) --cloud=gcp
	@echo "3. Procedure Generator:"
	docker run --rm datapipe/procedure-generator:latest --table-name=$(TABLE_NAME) --cloud=gcp --load-mode=incremental
	@echo "4. DAG Generator:"
	docker run --rm datapipe/dag-generator:latest --table-name=$(TABLE_NAME) --cloud=gcp --load-mode=incremental

clean:
	@echo "Limpiando..."
	@docker system prune -f
	@rm -rf output
	@echo "Limpieza completada"

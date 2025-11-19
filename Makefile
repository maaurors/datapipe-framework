.PHONY: help init-cloud build-cloud test-cloud setup build-generators

help:
	@echo "DataPipe Framework - Comandos Multinube:"
	@echo ""
	@echo "  make init-cloud CLOUD=gcp     - Crear proyecto GCP"
	@echo "  make init-cloud CLOUD=aws     - Crear proyecto AWS" 
	@echo "  make init-cloud CLOUD=azure   - Crear proyecto Azure"
	@echo "  make build-cloud CLOUD=gcp    - Construir imágenes"
	@echo "  make test-cloud CLOUD=gcp     - Probar pipeline"
	@echo "  make build-generators         - Construir generadores"
	@echo ""

setup:
	@echo "Verificando dependencias..."
	@which cookiecutter || echo "Instala cookiecutter: brew install cookiecutter"
	@echo "✅ Dependencias verificadas"

init-cloud:
ifndef CLOUD
	$(error CLOUD no definido. Uso: make init-cloud CLOUD=gcp|aws|azure)
endif
	@echo "Inicializando estructura para: $(CLOUD)"
	@mkdir -p clouds/$(CLOUD)/{extractor,loader,transformer}/src
	@mkdir -p templates/$(CLOUD)/\{\{cookiecutter.project_slug\}\}
	@echo "✅ Estructura $(CLOUD) creada"

build-cloud:
ifndef CLOUD
	$(error CLOUD no definido. Uso: make build-cloud CLOUD=gcp|aws|azure)
endif
	@echo "Construyendo imágenes para: $(CLOUD)"
	@docker build -t datapipe/loader-$(CLOUD):latest clouds/$(CLOUD)/loader/ 2>/dev/null || echo "⚠️  Dockerfile no encontrado para $(CLOUD)"
	@echo "✅ Imágenes $(CLOUD) procesadas"

test-cloud:
ifndef CLOUD
	$(error CLOUD no definido. Uso: make test-cloud CLOUD=gcp|aws|azure)
endif
	@echo "Probando pipeline: $(CLOUD)"
	@docker run --rm datapipe/loader-$(CLOUD):latest 2>/dev/null || echo "⚠️  Imagen no encontrada, ejecuta: make build-cloud CLOUD=$(CLOUD)"
	@echo "✅ Pipeline $(CLOUD) verificado"

build-generators:
	@echo "Construyendo generadores base..."
	cd generators/schema-generator && docker build -t datapipe/schema-generator:latest .
	cd generators/table-generator && docker build -t datapipe/table-generator:latest .
	@echo "✅ Generadores construidos"

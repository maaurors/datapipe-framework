# Guía de Inicio Rápido

Esta guía te llevará paso a paso desde la instalación hasta tu primera migración de datos.

## 1. Instalación del Entorno

Asegúrate de tener Docker y Poetry instalados.

```bash
# Verificar Docker
docker --version

# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

Clona el repositorio e instala las dependencias:

```bash
git clone https://github.com/maaurors/datapipe-framework.git
cd datapipe-framework
poetry install
```

## 2. Inicializando un Proyecto

El framework utiliza el concepto de "proyectos" para agrupar configuraciones de migración.

```bash
# Para Google Cloud Platform
poetry run datapipe init mi-proyecto-gcp --cloud gcp

# Para AWS
poetry run datapipe init mi-proyecto-aws --cloud aws

# Para Azure
poetry run datapipe init mi-proyecto-azure --cloud azure
```

Esto creará una carpeta con un archivo `config.yaml` base.

## 3. Configuración

Abre `mi-proyecto-gcp/config.yaml` y configura tu conexión a Oracle y destino.

> **Tip**: Usa variables de entorno `${VAR_NAME}` para credenciales sensibles. No las escribas directamente en el archivo.

```yaml
source:
  connection:
    host: "${DB_HOST}"
    user: "${DB_USER}"
    password: "${DB_PASSWORD}"
```

Define las tablas que quieres migrar:

```yaml
tables:
  - name: "CLIENTES"
    load_mode: "full"
  - name: "TRANSACCIONES"
    load_mode: "incremental"
    partition_column: "FECHA_TX"
```

## 4. Generación de Artefactos

El framework genera automáticamente todo el código necesario.

### Generar Schemas

Conecta a Oracle, lee los metadatos y crea archivos `.avsc` (AVRO) y `.json` (BigQuery).

```bash
poetry run datapipe generate schema CLIENTES --config mi-proyecto-gcp/config.yaml
```

### Generar DAGs

Crea el código Python para Airflow basado en templates probados.

```bash
poetry run datapipe generate dag CLIENTES --config mi-proyecto-gcp/config.yaml
```

## 5. Ejecución Local (Testing)

Puedes probar la extracción localmente usando Docker:

```bash
# Construir imágenes
make build

# Ejecutar extractor manualmente
docker run --env-file .env \
  -v $(pwd)/schemas:/app/schemas \
  datapipe/extractor:latest \
  --table CLIENTES \
  --cloud gcp
```

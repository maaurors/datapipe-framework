# DataPipe Framework

Framework profesional para migración de datos desde Oracle a múltiples clouds (GCP, AWS, Azure) utilizando una arquitectura moderna basada en Docker, AVRO y Poetry.

## Caracteristicas Principales

- **Multi-Cloud Nativo**: Soporte de primera clase para GCP (BigQuery), AWS (Redshift) y Azure (Synapse).
- **Arquitectura AVRO-First**: Todos los datos se extraen en formato AVRO con schema evolution y compresión Snappy.
- **Dockerizado**: Componentes aislados y portables (Extractor, Loader) con imágenes optimizadas (<200MB).
- **Gestión de Dependencias**: Uso de Poetry para builds reproducibles y seguros.
- **Generadores Automáticos**:
  - Schemas AVRO y JSON (BigQuery)
  - DAGs de Airflow
  - Scripts SQL
- **Configuración Centralizada**: Todo el proyecto se define en un simple `config.yaml`.

## Arquitectura Multi-Cloud

Este framework ha sido diseñado desde cero para ser agnóstico a la nube, permitiendo migrar datos a cualquier proveedor sin reescribir código.

### ¿Por qué es Multi-Cloud?

1.  **Abstracción de Lógica**: Los componentes de extracción (Oracle) y carga (Cloud) están desacoplados. El extractor genera archivos AVRO estándar que cualquier nube puede leer.
2.  **Configuración Unificada**: Un solo archivo `config.yaml` define el destino. Cambiar de GCP a AWS es tan simple como cambiar unas líneas de configuración.
3.  **Docker Containers**: Las imágenes de Docker reciben el parámetro `--cloud` y cargan dinámicamente las librerías necesarias (boto3 para AWS, google-cloud para GCP, azure-sdk para Azure).

### Integración de Nubes

-   **GCP**: Utiliza `google-cloud-storage` para staging y `google-cloud-bigquery` para la carga final. Soporta tablas particionadas y clustering.
-   **AWS**: Utiliza `boto3` para subir a S3 y comandos `COPY` para cargar en Redshift.
-   **Azure**: Utiliza `azure-storage-blob` para Data Lake Gen2 y `COPY` para Synapse Analytics.

## Automatización y Templates

El framework actúa como una fábrica de código automatizada.

1.  **Inicialización**: El comando `datapipe init` crea una estructura de carpetas estandarizada basada en templates Jinja2.
2.  **Generación de Código**:
    -   `datapipe generate schema`: Conecta a Oracle, lee los tipos de datos y genera automáticamente los schemas AVRO y de la nube destino.
    -   `datapipe generate dag`: Lee tu configuración y crea el código Python para Airflow, configurando los operadores Docker con las variables de entorno correctas.
3.  **Despliegue GitOps**: Al ser todo código generado, puedes versionarlo en Git. Tu CI/CD solo necesita ejecutar `make build` y copiar los DAGs generados a tu entorno de Airflow.

## DataPipe vs Pipelineer

| Característica | Pipelineer (Anterior) | DataPipe (Nuevo) |
| :--- | :--- | :--- |
| **Dependencias** | `pip` manual (propenso a conflictos) | `Poetry` (reproducible y seguro) |
| **Ejecución** | Depende del entorno local/Airflow | `Docker` (funciona igual en todas partes) |
| **Formato Datos** | CSV/JSON (lento, sin tipos) | `AVRO` (rápido, comprimido, tipado) |
| **Multi-Cloud** | Hardcoded para GCP | Diseño modular para GCP/AWS/Azure |
| **Mantenimiento** | Scripts dispersos | CLI unificada y estructura estándar |

## Requisitos Previos

- Python 3.11+
- Docker
- Poetry

## Quick Start

### 1. Instalación

```bash
git clone https://github.com/maaurors/datapipe-framework.git
cd datapipe-framework
poetry install
```

### 2. Crear un Nuevo Proyecto

```bash
# Inicializar proyecto para GCP
poetry run datapipe init migracion-ventas --cloud gcp
```

### 3. Configurar

Edita `migracion-ventas/config.yaml` con tus credenciales y tablas.

### 4. Generar Artefactos

```bash
# Generar schemas AVRO
poetry run datapipe generate schema VENTAS_2024 --config migracion-ventas/config.yaml

# Generar DAG de Airflow
poetry run datapipe generate dag VENTAS_2024 --config migracion-ventas/config.yaml
```

### 5. Build y Deploy

```bash
# Construir imágenes Docker
make build

# Desplegar DAGs a tu entorno Airflow
cp dags/* $AIRFLOW_HOME/dags/
```

## Documentación

- [Guía de Inicio Rápido](docs/getting-started.md)
- [Configuración Multi-Cloud](docs/multi-cloud.md)
- [Schemas AVRO y Tipos de Datos](docs/avro-schemas.md)

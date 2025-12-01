# Guía de Flujo de Trabajo: Migración Real Paso a Paso

Esta guía estandariza el proceso de uso del framework **DataPipe** para todo el equipo. Sigue estos pasos para garantizar migraciones exitosas y consistentes.

## Escenario de Ejemplo

Vamos a migrar el módulo de **Ventas** desde Oracle hacia **Google Cloud Platform (GCP)**.
- **Origen**: Oracle (Tablas `VENTAS_CABECERA`, `VENTAS_DETALLE`)
- **Destino**: BigQuery (Dataset `raw_ventas`)
- **Frecuencia**: Diaria

---

## Paso 1: Inicialización del Proyecto

Lo primero es crear el espacio de trabajo para este dominio de datos.

**Comando:**
```bash
poetry run datapipe init migracion-ventas --cloud gcp
```

**Resultado:**
Se crea la carpeta `migracion-ventas/` con la estructura base y un `config.yaml` plantilla.

---

## Paso 2: Configuración

Edita el archivo `migracion-ventas/config.yaml`. Aquí definimos *qué* vamos a mover y *hacia dónde*.

**Configuración de Conexión y Destino:**
Usa variables de entorno para las credenciales (nunca las escribas en el archivo).

```yaml
project:
  name: "migracion-ventas"
  environment: "production"

source:
  connection:
    host: "${ORACLE_HOST_PROD}"
    service_name: "ERP_PROD"
    user: "${ORACLE_USER}"
    password: "${ORACLE_PASSWORD}"

destination:
  cloud: "gcp"
  gcp:
    project_id: "empresa-datalake-prod"
    dataset: "raw_ventas"
    bucket: "empresa-staging-bucket"
    location: "us-central1"
```

**Definición de Tablas:**

```yaml
tables:
  - name: "VENTAS_CABECERA"
    load_mode: "incremental"    # Carga solo datos nuevos
    partition_column: "FECHA_VENTA"
    primary_keys: ["ID_VENTA"]

  - name: "VENTAS_DETALLE"
    load_mode: "incremental"
    partition_column: "FECHA_VENTA"
    primary_keys: ["ID_VENTA", "ID_DETALLE"]
```

---

## Paso 3: Generación de Schemas (AVRO)

El framework necesita entender la estructura de tus tablas para crear los archivos AVRO y las tablas en BigQuery.

**Comando:**
```bash
poetry run datapipe generate schema VENTAS_CABECERA --config migracion-ventas/config.yaml
poetry run datapipe generate schema VENTAS_DETALLE --config migracion-ventas/config.yaml
```

**Qué sucede por detrás:**
1.  Conecta a Oracle.
2.  Lee los metadatos de columnas y tipos.
3.  Genera `schemas/ventas_cabecera.avsc` (Schema AVRO estándar).
4.  Genera `schemas/ventas_cabecera.json` (Schema BigQuery).

---

## Paso 4: Generación de DAGs (Airflow)

Ahora creamos el código que orquestará la migración en Airflow.

**Comando:**
```bash
poetry run datapipe generate dag VENTAS_CABECERA --config migracion-ventas/config.yaml
poetry run datapipe generate dag VENTAS_DETALLE --config migracion-ventas/config.yaml
```

**Resultado:**
Se generan archivos Python en la carpeta `dags/`:
- `dags/dag_gcp_ventas_cabecera.py`
- `dags/dag_gcp_ventas_detalle.py`

Estos DAGs ya incluyen la lógica para usar los contenedores Docker de extracción y carga.

---

## Paso 5: Build y Validación

Antes de subir los cambios, aseguramos que todo esté correcto.

**Construir imágenes Docker:**
```bash
make build
```

**Validar localmente (opcional pero recomendado):**
Puedes probar una extracción de una tabla pequeña para verificar conectividad.
```bash
docker run --env-file .env datapipe/extractor:latest --table VENTAS_CABECERA --cloud gcp
```

---

## Paso 6: Despliegue (GitOps)

Finalmente, subimos nuestro trabajo al repositorio. El pipeline de CI/CD se encargará del resto.

```bash
git add migracion-ventas/ schemas/ dags/
git commit -m "Feat: Agrega migración de módulo de Ventas a GCP"
git push origin main
```

**En el servidor (Automático):**
1.  El CI construye las imágenes Docker y las sube al Registry (GCR/ECR).
2.  Los archivos de `dags/` se sincronizan con el bucket de DAGs de Cloud Composer/Airflow.

---

## Resumen de Comandos

| Paso | Acción | Comando |
| :--- | :--- | :--- |
| 1 | **Iniciar** | `poetry run datapipe init <nombre> --cloud <gcp|aws|azure>` |
| 2 | **Configurar** | Editar `config.yaml` |
| 3 | **Schemas** | `poetry run datapipe generate schema <table> --config <path>` |
| 4 | **DAGs** | `poetry run datapipe generate dag <table> --config <path>` |
| 5 | **Build** | `make build` |
| 6 | **Deploy** | `git push` |

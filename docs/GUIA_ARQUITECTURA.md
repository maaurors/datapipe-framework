# Guía de Arquitectura y Estrategia de Transformación

Esta guía responde a la pregunta clave: **"¿Qué herramienta uso y cuándo?"**

El framework **DataPipe** moderniza tu arquitectura pasando de un enfoque **ETL** (antiguo) a **ELT** (moderno).

---

## 1. El Cambio de Paradigma: De SPs a Dataform

### ❌ Antes (Pipelineer - ETL Tradicional)
1.  Extraía datos.
2.  Generaba un **Stored Procedure (SP)** complejo en PL/SQL o SQL.
3.  El SP transformaba y guardaba en una tabla **DEP** (Final).
4.  **Problema**: Difícil de testear, sin control de versiones real, lógica oculta en la base de datos.

### ✅ Ahora (DataPipe - Modern ELT)
1.  **Extract & Load (DataPipe)**: Mueve los datos de Oracle a la Nube (Capa **Staging/Raw**) tal cual vienen (AS-IS), en formato AVRO.
2.  **Transform (Dataform/dbt)**: Toma los datos de Staging y crea las tablas **DEP** (Finales) usando SQL modular y versionado.

---

## 2. ¿Qué hace DataPipe y qué NO hace?

| Capa | Responsable | Descripción |
| :--- | :--- | :--- |
| **Origen** | Oracle | Base de datos fuente. |
| **Extracción** | **DataPipe** | Genera AVROs. (Sí genera tabla Staging/Raw). |
| **Carga** | **DataPipe** | Sube a BigQuery/Redshift/Synapse (Capa Raw). |
| **Transformación** | **Dataform / dbt** | Limpieza, Joins, Lógica de Negocio. (Crea tablas DEP). |
| **Orquestación** | **Airflow** | Coordina que primero corra DataPipe y luego Dataform. |

> **Nota**: DataPipe **SÍ** crea la tabla de Staging (la llamamos "Raw"), pero **NO** genera Stored Procedures ni tablas DEP automáticamente. Esa responsabilidad se delega a herramientas especializadas en transformación como Dataform.

---

## 3. Árbol de Decisión: ¿Qué herramienta necesito?

Usa este diagrama para saber qué solicitar o crear.

### A. ¿Necesito mover datos de A a B?
*   **Sí, de Oracle a Nube (Batch)**: Usa **DataPipe**.
    *   *Resultado*: Datos en capa Raw/Staging.
*   **Sí, evento en tiempo real (ej. llega un archivo)**: Usa **Cloud Functions**.

### B. ¿Necesito limpiar, cruzar o agregar datos?
*   **Sí, en BigQuery/GCP**: Usa **Dataform**.
    *   Crea un repositorio Git para Dataform.
    *   Define tus tablas DEP como archivos `.sqlx`.
*   **Sí, en AWS/Azure**: Usa **dbt** (muy similar a Dataform).

### C. ¿Necesito ejecutar código complejo (Python/ML)?
*   **Sí**: Usa **Cloud Run** o **Kubernetes PodOperator** en Airflow.

---

## 4. Cómo integrar Dataform en tu Flujo

No necesitas hacerlo todo manual. Tu DAG de Airflow generado por DataPipe puede tener un paso extra.

**Flujo Sugerido:**

1.  **Repo 1 (Este framework)**: `datapipe-framework`
    *   Genera el DAG que hace: `Oracle -> GCS -> BigQuery Raw`.
2.  **Repo 2 (Lógica de Negocio)**: `dataform-ventas`
    *   Contiene la lógica SQL para transformar `Raw` a `DEP`.

**En Airflow:**
El DAG se vería así:
`[Extract Oracle] -> [Load BigQuery Raw] -> [Trigger Dataform Job]`

---

## 5. Resumen para el Usuario

*   **¿Cuándo uso DataPipe?**: Siempre que quieras traer datos "crudos" de Oracle.
*   **¿Cuándo pido un repo de Dataform?**: Cuando necesites crear tablas finales (DEP) con lógica de negocio, cruces o limpieza.
*   **¿Cuándo pido una Cloud Function?**: Casi nunca para cargas masivas. Solo para APIs ligeras o triggers de archivos individuales.

---

## 6. ¿Cómo ejecuto esta decisión? (El "Handshake")

Actualmente, el framework **DataPipe** no decide por ti, pero prepara el terreno para que la integración sea natural.

### Escenario Típico: "Necesito transformar datos"

1.  **Paso 1: Decisión (Humana)**
    *   Miras el árbol: "¿Necesito lógica compleja?" -> **SÍ**.
    *   Conclusión: Necesito **Dataform**.

2.  **Paso 2: Ejecución (Comandos)**
    *   **Ingesta**: Corres `datapipe init` y `generate dag`. Esto deja los datos en `dataset_raw.tabla_ventas`.
    *   **Transformación**: En otra terminal (o carpeta), inicias Dataform:
        ```bash
        dataform init dataform-ventas
        ```

3.  **Paso 3: El "Handshake" (Conexión)**
    *   En Dataform, declaras tu fuente (que DataPipe ya llenó):
        ```sql
        config { type: "declaration", schema: "dataset_raw", name: "tabla_ventas" }
        ```
    *   Ahora creas tu tabla final:
        ```sql
        config { type: "table", schema: "dataset_final", name: "ventas_dep" }
        SELECT * FROM ${ref("tabla_ventas")} WHERE monto > 0
        ```

### ¿Por qué repositorios separados?
Mantener `datapipe-framework` (Infraestructura/Ingesta) separado de `dataform-logica` (Negocio) permite que:
*   Los Ingenieros de Datos mantengan el DataPipe.
*   Los Analistas de BI/Data mantengan el Dataform (SQL) sin romper el pipeline de ingesta.

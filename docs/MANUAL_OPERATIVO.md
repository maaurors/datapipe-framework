# Manual Operativo: "Corta Palos" para Migraciones

Este documento es la guía definitiva paso a paso. Si sigues esto al pie de la letra, tu migración funcionará.

---

## 🟢 Paso 1: Iniciar el Proyecto (Solo una vez)

**Objetivo**: Crear la carpeta donde trabajarás.

1.  Abre tu terminal en la raíz del repositorio (`datapipe-framework`).
2.  Ejecuta el comando según tu nube destino:

    *   **Para GCP**:
        ```bash
        poetry run datapipe init migracion-gcp-ventas --cloud gcp
        ```
    *   **Para AWS**:
        ```bash
        poetry run datapipe init migracion-aws-logistica --cloud aws
        ```
    *   **Para Azure**:
        ```bash
        poetry run datapipe init migracion-azure-finanzas --cloud azure
        ```

    *(Cambia el nombre `migracion-xxx` por el nombre real de tu proyecto)*

---

## 🟡 Paso 2: Configuración (Donde ocurre la magia)

**Objetivo**: Decirle al framework qué tablas mover.

1.  Ve a la carpeta que se acaba de crear (ej. `migracion-gcp-ventas/`).
2.  Abre el archivo **`config.yaml`**.
3.  **Edita SOLO estas secciones**:

    *   **`source`**: Asegúrate de que las variables de entorno sean las correctas.
    *   **`destination`**: Pon el nombre real de tu Dataset (GCP), Schema (AWS) o Container (Azure).
    *   **`tables`**: Aquí es donde agregas tus tablas.

    ```yaml
    tables:
      - name: "VENTAS_2024"        # Nombre exacto en Oracle
        load_mode: "incremental"   # o "full"
        partition_column: "FECHA"  # Solo si es incremental
    ```

---

## 🟠 Paso 3: Generar Código (Automático)

**Objetivo**: Que el framework escriba el código por ti.

1.  Vuelve a la terminal (raíz del repo).
2.  Ejecuta estos 2 comandos por cada tabla que configuraste:

    **A. Generar Schema (Define la estructura)**
    ```bash
    poetry run datapipe generate schema VENTAS_2024 --config migracion-gcp-ventas/config.yaml
    ```
    *   👀 **Qué revisar**: Mira la carpeta `schemas/`. Debería aparecer `VENTAS_2024.avsc`.

    **B. Generar DAG (Define el proceso)**
    ```bash
    poetry run datapipe generate dag VENTAS_2024 --config migracion-gcp-ventas/config.yaml
    ```
    *   👀 **Qué revisar**: Mira la carpeta `dags/`. Debería aparecer un archivo `.py` nuevo.

---

## 🔵 Paso 4: Subir Cambios (Git Push)

**Objetivo**: Guardar tu trabajo y desplegar.

1.  En la terminal, verifica qué creaste:
    ```bash
    git status
    ```
    *(Deberías ver en rojo la carpeta de tu proyecto, los schemas y los dags)*

2.  Agrega todo:
    ```bash
    git add .
    ```

3.  Guarda con un mensaje claro:
    ```bash
    git commit -m "Feat: Agrego tabla VENTAS_2024 a GCP"
    ```

4.  Envía a la nube (GitHub):
    ```bash
    git push origin main
    ```

---

## 🟣 Resumen Visual de Carpetas

*   📂 **`datapipe-framework/`** (Raíz)
    *   📂 **`migracion-xxx/`** 👈 **AQUÍ TRABAJAS TÚ** (Editas `config.yaml`)
    *   📂 **`schemas/`** 👈 Aquí se generan archivos (Solo revisa, no toques)
    *   📂 **`dags/`** 👈 Aquí se genera el código Python (Solo revisa, no toques)
    *   📂 **`src/`** ⛔️ **PROHIBIDO TOCAR** (Es el cerebro del framework)
    *   📂 **`docker/`** ⛔️ **PROHIBIDO TOCAR** (Son los motores)

---

## 🆘 Solución de Problemas Comunes

*   **Error**: "Table not found in Oracle"
    *   **Solución**: Revisa el `config.yaml`, el nombre debe ser exacto (mayúsculas importan).
*   **Error**: "Credentials missing"
    *   **Solución**: Revisa que tengas las variables de entorno (`ORACLE_PASSWORD`, etc.) exportadas en tu terminal.

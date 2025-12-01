# Guía de Operación: Ambientes y Comandos Multi-Cloud

Esta guía responde a las preguntas frecuentes sobre cómo operar el framework en diferentes entornos (DEV/PRD) y nubes, y cómo la arquitectura Docker optimiza los costos.

## 1. Manejo de Ambientes (DEV vs PRD)

El framework está diseñado para que **el código y las imágenes Docker sean idénticos** en todos los ambientes. Lo único que cambia es la **configuración**.

### ¿Necesito comandos diferentes?
**No.** Los comandos de generación (`datapipe generate`) son los mismos. La diferencia se maneja a través de:
1.  **Archivos de Configuración**: Puedes tener `config_dev.yaml` y `config_prod.yaml`.
2.  **Variables de Entorno**: Es la práctica recomendada. Tu `config.yaml` usa variables que se inyectan en tiempo de ejecución.

### Ejemplo Práctico

**Archivo `config.yaml` (Único):**
```yaml
project:
  name: "migracion-ventas"
  environment: "${ENV}"  # Se llena con 'dev' o 'prod'

source:
  connection:
    host: "${DB_HOST}"   # En DEV apunta a Oracle DEV, en PRD a Oracle PRD
```

**Ejecución en DEV:**
```bash
export ENV=dev
export DB_HOST=oracle-dev.empresa.com
poetry run datapipe generate dag VENTAS --config config.yaml
```

**Ejecución en PRD:**
```bash
export ENV=prod
export DB_HOST=oracle-prod.empresa.com
poetry run datapipe generate dag VENTAS --config config.yaml
```

---

## 2. Comandos por Nube (GCP, AWS, Azure)

El CLI `datapipe` unifica la experiencia. No necesitas aprender comandos distintos para cada nube, solo cambiar el "flag" o la configuración.

### Inicialización
Aquí es donde decides la nube. Esto prepara la estructura correcta.

- **GCP**: `poetry run datapipe init proyecto-gcp --cloud gcp`
- **AWS**: `poetry run datapipe init proyecto-aws --cloud aws`
- **Azure**: `poetry run datapipe init proyecto-azure --cloud azure`

### Generación (Igual para todos)
Una vez inicializado, el comando es **idéntico**. El framework lee tu `config.yaml` y sabe qué hacer.

```bash
# Si tu config.yaml dice "cloud: aws", generará código para Redshift
poetry run datapipe generate dag VENTAS --config proyecto-aws/config.yaml

# Si tu config.yaml dice "cloud: azure", generará código para Synapse
poetry run datapipe generate dag VENTAS --config proyecto-azure/config.yaml
```

---

## 3. Normalización de Docker y Costos

Esta es la clave de la eficiencia del framework.

### Estrategia de "Imagen Única"
En lugar de tener una imagen para GCP, otra para AWS, etc., tenemos **imágenes normalizadas**:

1.  `datapipe/extractor:latest`: Sabe extraer de Oracle y guardar en CUALQUIER nube.
2.  `datapipe/loader:latest`: Sabe leer de CUALQUIER nube y cargar en su Data Warehouse.

### ¿Por qué es más económico?

1.  **Menos Almacenamiento**: Solo guardas 2 imágenes en tu Container Registry (aprox 200MB c/u), en lugar de docenas de imágenes específicas por pipeline.
2.  **Caché Eficiente**: Al usar la misma imagen base, los nodos de Kubernetes/Airflow cachean las capas. El arranque de los pods es casi instantáneo.
3.  **Mantenimiento**: Si actualizas la librería de Oracle, actualizas UNA imagen y todos los pipelines (GCP, AWS, Azure, Dev, Prod) se benefician automáticamente.

### Cómo funciona por dentro

Cuando el DAG de Airflow corre:

```python
# DAG generado automáticamente
DockerOperator(
    image='datapipe/extractor:latest',  # SIEMPRE la misma imagen
    command=["--cloud", "aws"],         # Aquí le decimos cómo comportarse
    environment={...}
)
```

La imagen recibe `--cloud aws` y activa internamente la lógica de S3. Si recibe `--cloud gcp`, activa GCS. **Es el mismo binario.**

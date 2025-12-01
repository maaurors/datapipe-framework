# Configuración Multi-Cloud

DataPipe soporta las tres nubes principales. Aquí se detallan los requisitos y configuraciones específicas para cada una.

## Google Cloud Platform (GCP)

### Requisitos
- Service Account con permisos:
  - `BigQuery Data Editor`
  - `Storage Object Admin`
- Bucket de GCS para staging
- Dataset de BigQuery creado

### Configuración (`config.yaml`)

```yaml
destination:
  cloud: "gcp"
  gcp:
    project_id: "mi-proyecto-gcp"
    dataset: "datalake_raw"
    bucket: "mi-bucket-staging"
    location: "us-central1"
```

---

## Amazon Web Services (AWS)

### Requisitos
- Credenciales AWS (Access Key / Secret Key) o IAM Role
- Permisos S3 y Redshift
- Cluster Redshift disponible

### Configuración (`config.yaml`)

```yaml
destination:
  cloud: "aws"
  aws:
    region: "us-east-1"
    s3_bucket: "mi-datalake-s3"
    redshift_cluster: "mi-cluster-redshift"
    redshift_db: "analytics"
    redshift_schema: "raw"
```

---

## Microsoft Azure

### Requisitos
- Azure Storage Account (Data Lake Gen2)
- Azure Synapse Analytics Workspace
- Service Principal con permisos de contribuidor

### Configuración (`config.yaml`)

```yaml
destination:
  cloud: "azure"
  azure:
    resource_group: "mi-resource-group"
    storage_account: "mistorageaccount"
    container: "raw-data"
    synapse_workspace: "mi-synapse"
    synapse_pool: "sqlpool1"
```

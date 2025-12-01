import os
import argparse
import structlog
from google.cloud import bigquery
import boto3
from azure.synapse.artifacts import ArtifactsClient

log = structlog.get_logger()

class Loader:
    def __init__(self, table_name: str, cloud: str, config_path: str):
        self.table_name = table_name
        self.cloud = cloud
        self.load_mode = os.getenv('LOAD_MODE', 'full')

    def load(self):
        log.info("Iniciando carga", table=self.table_name, cloud=self.cloud)
        
        if self.cloud == 'gcp':
            self._load_to_bigquery()
        elif self.cloud == 'aws':
            self._load_to_redshift()
        elif self.cloud == 'azure':
            self._load_to_synapse()

    def _load_to_bigquery(self):
        client = bigquery.Client()
        
        dataset_id = os.getenv('BQ_DATASET')
        table_id = f"{client.project}.{dataset_id}.{self.table_name}"
        
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.AVRO,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE if self.load_mode == 'full' else bigquery.WriteDisposition.WRITE_APPEND,
            autodetect=True,
        )

        uri = f"gs://{os.getenv('GCS_BUCKET')}/raw/{self.table_name}/*.avro"
        
        load_job = client.load_table_from_uri(
            uri, table_id, job_config=job_config
        )
        
        load_job.result()  # Waits for the job to complete.
        log.info("Carga a BigQuery completada", table=table_id)

    def _load_to_redshift(self):
        # Implementación simplificada para Redshift COPY command
        log.info("Cargando a Redshift desde S3...")
        # TODO: Implementar psycopg2 COPY command

    def _load_to_synapse(self):
        # Implementación simplificada para Synapse COPY
        log.info("Cargando a Synapse desde Blob Storage...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--table', required=True)
    parser.add_argument('--cloud', required=True)
    parser.add_argument('--config', default='/config/config.yaml')
    args = parser.parse_args()
    
    loader = Loader(args.table, args.cloud, args.config)
    loader.load()

#!/usr/bin/env python3
"""Loader - Carga datos a BigQuery desde GCS"""

from google.cloud import bigquery
import structlog

log = structlog.get_logger()

class BigQueryLoader:
    def __init__(self):
        self.client = bigquery.Client()
    
    def load_from_gcs(self, gcs_uri, table_id):
        """Cargar datos desde GCS a BigQuery"""
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.AVRO,
        )
        
        load_job = self.client.load_table_from_uri(
            gcs_uri, table_id, job_config=job_config
        )
        
        load_job.result()  # Esperar a que termine
        log.info("Datos cargados a BigQuery", table=table_id)

if __name__ == '__main__':
    loader = BigQueryLoader()
    loader.load_from_gcs("gs://my-bucket/data.avro", "my-project.dataset.table")

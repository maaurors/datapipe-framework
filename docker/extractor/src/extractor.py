import os
import argparse
import oracledb
import fastavro
import structlog
from datetime import datetime
from google.cloud import storage
import boto3
from azure.storage.blob import BlobServiceClient

log = structlog.get_logger()

class Extractor:
    def __init__(self, table_name: str, cloud: str, config_path: str):
        self.table_name = table_name
        self.cloud = cloud
        # TODO: Load full config
        self.batch_size = 10000

    def extract(self):
        log.info("Iniciando extracción", table=self.table_name, cloud=self.cloud)
        
        # Conexión a Oracle (usando variables de entorno por ahora)
        dsn = oracledb.makedsn(
            os.getenv('ORACLE_HOST', 'localhost'),
            os.getenv('ORACLE_PORT', '1521'),
            service_name=os.getenv('ORACLE_SERVICE')
        )
        
        try:
            with oracledb.connect(
                user=os.getenv('ORACLE_USER'),
                password=os.getenv('ORACLE_PASSWORD'),
                dsn=dsn
            ) as connection:
                with connection.cursor() as cursor:
                    self._process_table(cursor)
        except Exception as e:
            log.error("Error en extracción", error=str(e))
            raise

    def _process_table(self, cursor):
        query = f"SELECT * FROM {self.table_name}"
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        
        # Schema AVRO (debería cargarse del archivo generado)
        schema = {
            "type": "record",
            "name": self.table_name,
            "fields": [{"name": col, "type": ["null", "string"]} for col in columns]
        }

        batch_num = 0
        while True:
            rows = cursor.fetchmany(self.batch_size)
            if not rows:
                break
                
            self._write_batch(rows, columns, schema, batch_num)
            batch_num += 1

    def _write_batch(self, rows, columns, schema, batch_num):
        # Convertir a lista de dicts
        data = [dict(zip(columns, row)) for row in rows]
        
        filename = f"{self.table_name}_{batch_num}.avro"
        
        # Escribir AVRO local
        with open(filename, 'wb') as out:
            fastavro.writer(out, schema, data, codec='snappy')
            
        # Subir a Cloud
        self._upload_to_cloud(filename)
        os.remove(filename)
        log.info("Batch procesado", batch=batch_num, rows=len(rows))

    def _upload_to_cloud(self, filename):
        if self.cloud == 'gcp':
            client = storage.Client()
            bucket = client.bucket(os.getenv('GCS_BUCKET'))
            blob = bucket.blob(f"raw/{self.table_name}/{filename}")
            blob.upload_from_filename(filename)
        elif self.cloud == 'aws':
            s3 = boto3.client('s3')
            s3.upload_file(filename, os.getenv('S3_BUCKET'), f"raw/{self.table_name}/{filename}")
        elif self.cloud == 'azure':
            service = BlobServiceClient.from_connection_string(os.getenv('AZURE_CONN_STR'))
            blob = service.get_blob_client(container=os.getenv('AZURE_CONTAINER'), blob=f"raw/{self.table_name}/{filename}")
            with open(filename, "rb") as data:
                blob.upload_blob(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--table', required=True)
    parser.add_argument('--cloud', required=True)
    parser.add_argument('--config', default='/config/config.yaml')
    args = parser.parse_args()
    
    extractor = Extractor(args.table, args.cloud, args.config)
    extractor.extract()

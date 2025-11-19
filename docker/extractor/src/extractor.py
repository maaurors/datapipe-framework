#!/usr/bin/env python3
"""Extractor - Extrae datos de Oracle a GCS"""

import oracledb
from google.cloud import storage
import structlog

log = structqlog.get_logger()

class OracleExtractor:
    def extract_to_gcs(self, query, gcs_path):
        """Extraer datos de Oracle y subir a GCS"""
        # Conexión a Oracle
        connection = oracledb.connect(user="user", password="pass", dsn="dsn")
        
        # Ejecutar query y extraer datos
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        
        # Subir a GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket("my-bucket")
        blob = bucket.blob(gcs_path)
        blob.upload_from_string(str(data))
        
        log.info("Datos extraídos y subidos", rows=len(data), path=gcs_path)

if __name__ == '__main__':
    extractor = OracleExtractor()
    extractor.extract_to_gcs("SELECT * FROM my_table", "extracts/data.csv")

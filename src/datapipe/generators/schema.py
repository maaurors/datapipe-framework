import json
from pathlib import Path
from typing import Dict, List, Any
import structlog
from datapipe.config.loader import ProjectConfig

log = structlog.get_logger()

class SchemaGenerator:
    """Generador de schemas AVRO y Cloud (BigQuery/Redshift/Synapse)"""
    
    ORACLE_TO_AVRO = {
        'VARCHAR2': 'string',
        'NVARCHAR2': 'string',
        'CHAR': 'string',
        'NUMBER': 'double',
        'DATE': 'long',  # timestamp-millis
        'TIMESTAMP': 'long',
        'CLOB': 'string',
        'BLOB': 'bytes'
    }

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.output_dir = Path('schemas')
        self.output_dir.mkdir(exist_ok=True)

    def generate(self, table_name: str):
        """Generar schemas para una tabla"""
        log.info("Generando schemas", table=table_name)
        
        # En una implementación real, aquí conectaríamos a Oracle
        # para obtener metadatos:
        # columns = self.oracle_client.get_columns(table_name)
        
        # Mock para demostración
        columns = [
            {'name': 'ID', 'type': 'NUMBER', 'nullable': False},
            {'name': 'NOMBRE', 'type': 'VARCHAR2', 'nullable': True},
            {'name': 'FECHA_CREACION', 'type': 'TIMESTAMP', 'nullable': True}
        ]
        
        self._generate_avro(table_name, columns)
        self._generate_cloud_schema(table_name, columns)

    def _generate_avro(self, table_name: str, columns: List[Dict]):
        """Generar archivo .avsc"""
        fields = []
        for col in columns:
            avro_type = self.ORACLE_TO_AVRO.get(col['type'], 'string')
            
            if col['type'] in ['DATE', 'TIMESTAMP']:
                type_def = {'type': 'long', 'logicalType': 'timestamp-millis'}
            else:
                type_def = avro_type

            if col['nullable']:
                type_def = ['null', type_def]

            fields.append({
                'name': col['name'].lower(),
                'type': type_def
            })

        schema = {
            'type': 'record',
            'name': table_name.lower(),
            'namespace': 'oracle.schema',
            'fields': fields
        }

        output_path = self.output_dir / f"{table_name.lower()}.avsc"
        with open(output_path, 'w') as f:
            json.dump(schema, f, indent=2)
        
        log.info("Schema AVRO generado", path=str(output_path))

    def _generate_cloud_schema(self, table_name: str, columns: List[Dict]):
        """Generar schema específico de la nube (ej. BigQuery JSON)"""
        if self.config.destination.cloud == 'gcp':
            self._generate_bigquery_schema(table_name, columns)
        # TODO: Implementar AWS/Azure

    def _generate_bigquery_schema(self, table_name: str, columns: List[Dict]):
        bq_schema = []
        for col in columns:
            bq_type = 'STRING'
            if col['type'] == 'NUMBER':
                bq_type = 'NUMERIC'
            elif col['type'] in ['DATE', 'TIMESTAMP']:
                bq_type = 'TIMESTAMP'
            
            bq_schema.append({
                'name': col['name'].lower(),
                'type': bq_type,
                'mode': 'NULLABLE' if col['nullable'] else 'REQUIRED'
            })

        output_path = self.output_dir / f"{table_name.lower()}.json"
        with open(output_path, 'w') as f:
            json.dump(bq_schema, f, indent=2)
            
        log.info("Schema BigQuery generado", path=str(output_path))

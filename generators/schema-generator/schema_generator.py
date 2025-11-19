#!/usr/bin/env python3
"""Schema Generator - Genera schemas AVRO y JSON desde Oracle"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

class SchemaGenerator:
    """Generador de schemas"""
    
    TYPE_MAPPING = {
        'VARCHAR2': 'string',
        'NUMBER': 'double',
        'DATE': 'string',
        'TIMESTAMP': 'string',
        'CLOB': 'string',
        'BLOB': 'bytes',
    }
    
    BQ_TYPE_MAPPING = {
        'VARCHAR2': 'STRING',
        'NUMBER': 'NUMERIC',
        'DATE': 'TIMESTAMP',
        'TIMESTAMP': 'TIMESTAMP',
        'CLOB': 'STRING',
        'BLOB': 'BYTES',
    }
    
    def __init__(self):
        self.oracle_table = os.getenv('ORACLE_TABLE', 'TEST_TABLE')
        self.output_dir = Path('/output')
        print(f"Schema Generator iniciado para tabla: {self.oracle_table}")
    
    def generate_mock_columns(self) -> List[Dict[str, Any]]:
        """Generar columnas mock para demo"""
        return [
            {'name': 'ID', 'data_type': 'NUMBER', 'nullable': False},
            {'name': 'NAME', 'data_type': 'VARCHAR2', 'nullable': True},
            {'name': 'CREATED_AT', 'data_type': 'TIMESTAMP', 'nullable': True},
        ]
    
    def oracle_to_avro_type(self, column: Dict) -> Any:
        """Convertir tipo Oracle a AVRO"""
        base_type = self.TYPE_MAPPING.get(column['data_type'], 'string')
        if column['nullable']:
            return ['null', base_type]
        return base_type
    
    def generate_avro_schema(self, columns: List[Dict]) -> Dict:
        """Generar schema AVRO"""
        fields = [
            {
                'name': col['name'].lower(),
                'type': self.oracle_to_avro_type(col),
                'doc': f"Oracle type: {col['data_type']}"
            }
            for col in columns
        ]
        
        return {
            'type': 'record',
            'name': self.oracle_table.lower(),
            'namespace': 'oracle.schema',
            'fields': fields
        }
    
    def generate_bigquery_schema(self, columns: List[Dict]) -> List[Dict]:
        """Generar schema BigQuery"""
        return [
            {
                'name': col['name'].lower(),
                'type': self.BQ_TYPE_MAPPING.get(col['data_type'], 'STRING'),
                'mode': 'NULLABLE' if col['nullable'] else 'REQUIRED'
            }
            for col in columns
        ]
    
    def save_schemas(self, avro_schema: Dict, bq_schema: List[Dict]):
        """Guardar schemas en archivos"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        table_name = self.oracle_table.lower()
        
        avro_file = self.output_dir / f'{table_name}.avsc'
        with open(avro_file, 'w') as f:
            json.dump(avro_schema, f, indent=2)
        print(f"AVRO schema: {avro_file}")
        
        bq_file = self.output_dir / f'{table_name}.json'
        with open(bq_file, 'w') as f:
            json.dump(bq_schema, f, indent=2)
        print(f"BigQuery schema: {bq_file}")
    
    def run(self):
        """Ejecutar generacion"""
        try:
            print("Generando schemas...")
            columns = self.generate_mock_columns()
            avro_schema = self.generate_avro_schema(columns)
            bq_schema = self.generate_bigquery_schema(columns)
            self.save_schemas(avro_schema, bq_schema)
            print("Schemas generados exitosamente")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    generator = SchemaGenerator()
    generator.run()

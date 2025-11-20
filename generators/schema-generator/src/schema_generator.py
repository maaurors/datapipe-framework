#!/usr/bin/env python3
"""Generic Schema Generator for DataPipe Framework"""

import json
import yaml
import structlog
from typing import Dict, List, Any
import argparse

log = structlog.get_logger()

class GenericSchemaGenerator:
    def __init__(self, table_name: str = "", cloud: str = "gcp"):
        self.table_name = table_name
        self.cloud = cloud
        
    def generate_avro_schema(self, columns: List[Dict]) -> Dict[str, Any]:
        """Generate generic AVRO schema from column definitions"""
        fields = []
        
        for col in columns:
            field = {
                "name": col.get("name", "").lower(),
                "type": self._map_data_type(col.get("type", "string"), "avro"),
                "doc": col.get("description", f"Column {col.get('name', '')}")
            }
            
            # Handle nullability
            if col.get("nullable", True):
                field["type"] = ["null", field["type"]]
                
            fields.append(field)
        
        schema = {
            "type": "record",
            "name": f"{self.table_name}_record" if self.table_name else "generic_record",
            "namespace": "com.datapipe.generated",
            "fields": fields
        }
        
        log.info("AVRO schema generated", table=self.table_name, fields_count=len(fields))
        return schema
    
    def generate_json_config(self, columns: List[Dict]) -> Dict[str, Any]:
        """Generate generic JSON configuration"""
        config = {
            "table_name": self.table_name,
            "cloud_provider": self.cloud,
            "load_mode": "incremental",  # Default
            "columns": [
                {
                    "name": col.get("name", "").lower(),
                    "type": self._map_data_type(col.get("type", "string"), "json"),
                    "description": col.get("description", ""),
                    "nullable": col.get("nullable", True)
                }
                for col in columns
            ],
            "partitioning": {
                "field": "fecha_creacion",
                "type": "DAY"
            },
            "clustering": ["id", "estado"]
        }
        return config
    
    def _map_data_type(self, source_type: str, target_format: str) -> str:
        """Map source data types to target format types"""
        mapping = {
            "avro": {
                "VARCHAR2": "string",
                "NVARCHAR2": "string", 
                "CHAR": "string",
                "NCHAR": "string",
                "NUMBER": "double",
                "INTEGER": "int",
                "FLOAT": "float",
                "DATE": "string",
                "TIMESTAMP": "string",
                "CLOB": "string",
                "BLOB": "bytes"
            },
            "json": {
                "VARCHAR2": "STRING",
                "NVARCHAR2": "STRING",
                "CHAR": "STRING", 
                "NCHAR": "STRING",
                "NUMBER": "NUMERIC",
                "INTEGER": "INT64",
                "FLOAT": "FLOAT64",
                "DATE": "DATE",
                "TIMESTAMP": "TIMESTAMP",
                "CLOB": "STRING",
                "BLOB": "BYTES"
            }
        }
        
        return mapping[target_format].get(source_type.upper(), "string")
    
    def generate_sample_output(self):
        """Generate sample schemas and print to stdout"""
        log.info("Generating sample schemas", table=self.table_name)
        
        # Sample columns - in real implementation, this would come from Oracle
        sample_columns = [
            {"name": "ID", "type": "NUMBER", "nullable": False, "description": "Primary key"},
            {"name": "NOMBRE", "type": "VARCHAR2", "nullable": False, "description": "Name field"},
            {"name": "FECHA_CREACION", "type": "DATE", "nullable": False, "description": "Creation date"},
            {"name": "ESTADO", "type": "VARCHAR2", "nullable": True, "description": "Status field"}
        ]
        
        avro_schema = self.generate_avro_schema(sample_columns)
        json_config = self.generate_json_config(sample_columns)
        
        print("=== AVRO SCHEMA ===")
        print(json.dumps(avro_schema, indent=2))
        print("\n=== JSON CONFIG ===")
        print(json.dumps(json_config, indent=2))
        
        log.info("Schemas generated successfully")

def main():
    """Main function for Docker container"""
    parser = argparse.ArgumentParser(description='Generic Schema Generator')
    parser.add_argument('--table-name', type=str, help='Table name')
    parser.add_argument('--cloud', type=str, default='gcp', help='Cloud provider')
    
    args = parser.parse_args()
    
    generator = GenericSchemaGenerator(
        table_name=args.table_name or "generic_table",
        cloud=args.cloud
    )
    
    # Generate sample schemas
    generator.generate_sample_output()

if __name__ == "__main__":
    main()

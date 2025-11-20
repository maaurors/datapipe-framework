#!/usr/bin/env python3
"""Azure Extractor for DataPipe Framework - Oracle to Azure Storage"""

import argparse
import json

class AzureExtractor:
    def __init__(self, table_name: str = ""):
        self.table_name = table_name
        
    def extract_from_oracle_to_storage(self):
        """Extract data from Oracle and upload to Azure Storage"""
        print(f"Azure Extractor: Extracting table {self.table_name} from Oracle")
        
        # Simular conexión a Oracle
        print("Connecting to Oracle database...")
        
        # Simular extracción de datos
        sample_data = [
            {"id": 1, "nombre": "Ejemplo Azure 1", "fecha_creacion": "2024-01-01"},
            {"id": 2, "nombre": "Ejemplo Azure 2", "fecha_creacion": "2024-01-02"}
        ]
        
        # Convertir a JSON
        data_json = json.dumps(sample_data, indent=2)
        
        # Subir a Azure Storage
        blob_name = f"raw/{self.table_name}/data.json"
        print(f"Uploading to Azure Storage: {blob_name}")
        
        print("Data successfully uploaded to Azure Storage")
        print(f"Azure Storage Path: https://mystorage.blob.core.windows.net/mycontainer/{blob_name}")
        
    def extract_from_api_to_storage(self):
        """Extract data from API and upload to Azure Storage"""
        print(f"Azure Extractor: Extracting API data for {self.table_name}")
        print("Calling Azure API endpoint...")
        print("Converting to Parquet format...")
        print("Uploading to Azure Storage...")
        print("API data extraction completed")

def main():
    parser = argparse.ArgumentParser(description='Azure Extractor')
    parser.add_argument('--table-name', type=str, required=True, help='Table name')
    parser.add_argument('--source', type=str, choices=['oracle', 'api'], default='oracle', help='Data source')
    
    args = parser.parse_args()
    
    extractor = AzureExtractor(table_name=args.table_name)
    
    if args.source == 'oracle':
        extractor.extract_from_oracle_to_storage()
    else:
        extractor.extract_from_api_to_storage()

if __name__ == "__main__":
    main()

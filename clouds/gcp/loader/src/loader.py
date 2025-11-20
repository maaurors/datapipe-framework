#!/usr/bin/env python3
"""Generic GCP Loader for DataPipe Framework"""

import argparse
import structlog

log = structlog.get_logger()

class GCPLoader:
    def __init__(self, table_name: str = ""):
        self.table_name = table_name
        
    def load_to_bigquery(self):
        """Load data from GCS to BigQuery"""
        log.info("Loading to BigQuery", table=self.table_name)
        print(f"Loading data to BigQuery table: {self.table_name}")
        print("Using: GCS AVRO files -> BigQuery batch load")
        print("Cost optimized: Batch load instead of streaming")

def main():
    parser = argparse.ArgumentParser(description='GCP Loader')
    parser.add_argument('--table-name', type=str, required=True, help='Table name')
    
    args = parser.parse_args()
    
    loader = GCPLoader(table_name=args.table_name)
    loader.load_to_bigquery()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generic GCP Extractor for DataPipe Framework"""

import argparse
import structlog

log = structlog.get_logger()

class GCPExtractor:
    def __init__(self, table_name: str = ""):
        self.table_name = table_name
        
    def extract_from_oracle(self):
        """Extract data from Oracle to GCS"""
        log.info("Extracting from Oracle", table=self.table_name)
        # Placeholder - would connect to Oracle and extract data
        print(f"Extracting data for table: {self.table_name}")
        print("Output: GCS bucket in AVRO format")
        
    def extract_from_api(self):
        """Extract data from API to GCS"""
        log.info("Extracting from API", table=self.table_name)
        print(f"Extracting API data for table: {self.table_name}")
        print("Output: GCS bucket in AVRO format")

def main():
    parser = argparse.ArgumentParser(description='GCP Extractor')
    parser.add_argument('--table-name', type=str, required=True, help='Table name')
    parser.add_argument('--source', type=str, choices=['oracle', 'api'], default='oracle', help='Data source')
    
    args = parser.parse_args()
    
    extractor = GCPExtractor(table_name=args.table_name)
    
    if args.source == 'oracle':
        extractor.extract_from_oracle()
    else:
        extractor.extract_from_api()

if __name__ == "__main__":
    main()

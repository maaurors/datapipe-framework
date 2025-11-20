#!/usr/bin/env python3
"""Generic GCP Transformer for DataPipe Framework"""

import argparse
import structlog

log = structlog.get_logger()

class GCPTransformer:
    def __init__(self, table_name: str = "", load_mode: str = "incremental"):
        self.table_name = table_name
        self.load_mode = load_mode
        
    def execute_stored_procedure(self):
        """Execute stored procedure for transformation"""
        log.info("Executing transformation", table=self.table_name, mode=self.load_mode)
        print(f"Executing stored procedure for table: {self.table_name}")
        print(f"Load mode: {self.load_mode}")
        if self.load_mode == "incremental":
            print("Procedure: MERGE/UPSERT operation")
        else:
            print("Procedure: TRUNCATE + LOAD operation")

def main():
    parser = argparse.ArgumentParser(description='GCP Transformer')
    parser.add_argument('--table-name', type=str, required=True, help='Table name')
    parser.add_argument('--load-mode', type=str, choices=['full', 'incremental'], default='incremental', help='Load mode')
    
    args = parser.parse_args()
    
    transformer = GCPTransformer(table_name=args.table_name, load_mode=args.load_mode)
    transformer.execute_stored_procedure()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generic Procedure Generator for DataPipe Framework"""

import argparse

class GenericProcedureGenerator:
    def __init__(self, table_name: str = "", cloud: str = "gcp", load_mode: str = "incremental"):
        self.table_name = table_name
        self.cloud = cloud
        self.load_mode = load_mode
        
    def generate_merge_procedure(self) -> str:
        if self.load_mode == "incremental":
            return self._generate_upsert_procedure()
        else:
            return self._generate_truncate_load_procedure()
    
    def _generate_upsert_procedure(self) -> str:
        procedure = f"CREATE OR REPLACE PROCEDURE project.dataset.sp_merge_dep_{self.table_name}()\n"
        procedure += "OPTIONS (strict_mode = FALSE)\n"
        procedure += "BEGIN\n"
        procedure += f"  MERGE INTO project.dataset.dep_{self.table_name} AS destino\n"
        procedure += f"  USING project.dataset.stg_{self.table_name} AS origen\n"
        procedure += "  ON destino.id = origen.id\n"
        procedure += "  WHEN MATCHED THEN\n"
        procedure += "    UPDATE SET\n"
        procedure += "      destino.nombre = origen.nombre,\n"
        procedure += "      destino.fecha_creacion = origen.fecha_creacion\n"
        procedure += "  WHEN NOT MATCHED THEN\n"
        procedure += "    INSERT (id, nombre, fecha_creacion)\n"
        procedure += "    VALUES (origen.id, origen.nombre, origen.fecha_creacion);\n"
        procedure += "END;"
        return procedure
    
    def _generate_truncate_load_procedure(self) -> str:
        procedure = f"CREATE OR REPLACE PROCEDURE project.dataset.sp_load_dep_{self.table_name}()\n"
        procedure += "BEGIN\n"
        procedure += f"  DELETE FROM project.dataset.dep_{self.table_name} WHERE TRUE;\n"
        procedure += f"  INSERT INTO project.dataset.dep_{self.table_name}\n"
        procedure += f"  SELECT * FROM project.dataset.stg_{self.table_name};\n"
        procedure += "END;"
        return procedure

def main():
    parser = argparse.ArgumentParser(description='Generic Procedure Generator')
    parser.add_argument('--table-name', type=str, help='Table name')
    parser.add_argument('--cloud', type=str, default='gcp', help='Cloud provider')
    parser.add_argument('--load-mode', type=str, default='incremental', help='Load mode')
    
    args = parser.parse_args()
    
    generator = GenericProcedureGenerator(
        table_name=args.table_name or "generic_table",
        cloud=args.cloud,
        load_mode=args.load_mode
    )
    
    procedure = generator.generate_merge_procedure()
    print("=== STORED PROCEDURE ===")
    print(procedure)

if __name__ == "__main__":
    main()

from cloud_migrator.core.base_migrator import BaseCloudMigrator

class GCPDataflowMigrator(BaseCloudMigrator):
    def extract_from_oracle(self, table_name):
        print(f"Extrayendo {table_name} de Oracle para GCP")
        return f"data_from_{table_name}"
    
    def transform_data(self, data):
        print(f"Transformando datos para GCP: {data}")
        return f"transformed_{data}"
    
    def load_to_cloud(self, data, destination):
        print(f"Cargando {data} a BigQuery: {destination}")
    
    def run_dataflow_job(self, table_name, destination):
        """Ejecutar migración completa para GCP"""
        print(f" Ejecutando Dataflow job para {table_name}")
        self.migrate(table_name, destination)

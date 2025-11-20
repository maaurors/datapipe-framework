from cloud_migrator.core.base_migrator import BaseCloudMigrator

class AWSGlueMigrator(BaseCloudMigrator):
    def extract_from_oracle(self, table_name):
        print(f"Extrayendo {table_name} de Oracle para AWS")
        return f"data_from_{table_name}"
    
    def transform_data(self, data):
        print(f"Transformando datos para AWS: {data}")
        return f"transformed_{data}"
    
    def load_to_cloud(self, data, destination):
        print(f"Cargando {data} a Redshift/S3: {destination}")
    
    def run_glue_job(self, table_name, destination):
        """Ejecutar migración completa para AWS"""
        print(f" Ejecutando Glue job para {table_name}")
        self.migrate(table_name, destination)

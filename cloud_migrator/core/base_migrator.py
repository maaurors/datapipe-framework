from abc import ABC, abstractmethod
import logging

class BaseCloudMigrator(ABC):
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def extract_from_oracle(self, table_name):
        """Extraer datos de Oracle"""
        pass
    
    @abstractmethod
    def transform_data(self, data):
        """Transformar datos"""
        pass
    
    @abstractmethod
    def load_to_cloud(self, data, destination):
        """Cargar datos al cloud"""
        pass
    
    def migrate(self, table_name, destination):
        """Pipeline completo de migración"""
        self.logger.info(f"Iniciando migración: {table_name} → {destination}")
        
        # Extraer
        data = self.extract_from_oracle(table_name)
        
        # Transformar
        transformed_data = self.transform_data(data)
        
        # Cargar
        self.load_to_cloud(transformed_data, destination)
        
        self.logger.info("Migración completada")

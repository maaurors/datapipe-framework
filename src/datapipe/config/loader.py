import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ConnectionConfig(BaseModel):
    host: str
    port: int = 1521
    service_name: str
    user: str
    password: str

class SourceConfig(BaseModel):
    type: str = "oracle"
    connection: ConnectionConfig

class DestinationConfig(BaseModel):
    cloud: str
    # Configs específicas por cloud
    gcp: Optional[Dict[str, Any]] = None
    aws: Optional[Dict[str, Any]] = None
    azure: Optional[Dict[str, Any]] = None

class TableConfig(BaseModel):
    name: str
    load_mode: str = "full"
    partition_column: Optional[str] = None
    primary_keys: List[str] = []

class ProjectConfig(BaseModel):
    name: str
    environment: str = "dev"
    source: SourceConfig
    destination: DestinationConfig
    tables: List[TableConfig]

class ConfigLoader:
    @staticmethod
    def load(path: str) -> ProjectConfig:
        """Cargar y validar configuración desde YAML"""
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
            
        with open(config_path, 'r') as f:
            raw_config = yaml.safe_load(f)
            
        # Aquí se podría implementar lógica para reemplazar secrets
        # ej. ${SECRET:name} -> valor real
        
        return ProjectConfig(**raw_config)

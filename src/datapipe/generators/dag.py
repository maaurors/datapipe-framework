from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import structlog
from datapipe.config.loader import ProjectConfig

log = structlog.get_logger()

class DagGenerator:
    """Generador de DAGs de Airflow"""
    
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.output_dir = Path('dags')
        self.output_dir.mkdir(exist_ok=True)
        
        # Configurar Jinja2
        template_dir = Path(__file__).parent.parent.parent.parent / 'templates' / 'dags'
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

    def generate(self, table_name: str):
        """Generar DAG para una tabla"""
        log.info("Generando DAG", table=table_name, cloud=self.config.destination.cloud)
        
        template_name = f"oracle_to_{self.config.destination.cloud}.py.j2"
        try:
            template = self.env.get_template(template_name)
        except Exception:
            # Fallback a template genérico si no existe
            log.warning(f"Template {template_name} no encontrado, usando generic")
            return

        # Encontrar config de la tabla
        table_config = next((t for t in self.config.tables if t.name == table_name), None)
        if not table_config:
            raise ValueError(f"Tabla {table_name} no encontrada en config")

        dag_content = template.render(
            project=self.config,
            table=table_config,
            schedule="@daily" # TODO: Configurable
        )

        output_path = self.output_dir / f"dag_{self.config.destination.cloud}_{table_name.lower()}.py"
        with open(output_path, 'w') as f:
            f.write(dag_content)
            
        log.info("DAG generado", path=str(output_path))

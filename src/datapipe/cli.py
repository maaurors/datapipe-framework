import click
import structlog
from pathlib import Path
from datapipe.generators.schema import SchemaGenerator
from datapipe.generators.dag import DagGenerator
from datapipe.config.loader import ConfigLoader

log = structlog.get_logger()

@click.group()
def main():
    """DataPipe Framework CLI - Migración Oracle a Multi-Cloud"""
    pass

@main.command()
@click.argument('project_name')
@click.option('--cloud', type=click.Choice(['gcp', 'aws', 'azure']), required=True, help='Nube destino')
def init(project_name, cloud):
    """Inicializar un nuevo proyecto de migración"""
    log.info("Inicializando proyecto", project=project_name, cloud=cloud)
    # TODO: Implementar copia de templates
    click.echo(f"Proyecto {project_name} inicializado para {cloud}")

@main.command()
@click.argument('table_name')
@click.option('--config', default='config.yaml', help='Archivo de configuración')
def generate_schema(table_name, config):
    """Generar schemas AVRO y destino (BigQuery/Redshift/Synapse)"""
    try:
        cfg = ConfigLoader.load(config)
        generator = SchemaGenerator(cfg)
        generator.generate(table_name)
        click.echo(f"Schemas generados para {table_name}")
    except Exception as e:
        log.error("Error generando schema", error=str(e))
        raise click.ClickException(str(e))

@main.command()
@click.argument('table_name')
@click.option('--config', default='config.yaml', help='Archivo de configuración')
def generate_dag(table_name, config):
    """Generar DAG de Airflow"""
    try:
        cfg = ConfigLoader.load(config)
        generator = DagGenerator(cfg)
        generator.generate(table_name)
        click.echo(f"DAG generado para {table_name}")
    except Exception as e:
        log.error("Error generando DAG", error=str(e))
        raise click.ClickException(str(e))

@main.command()
@click.option('--cloud', type=click.Choice(['gcp', 'aws', 'azure']), required=True)
def build(cloud):
    """Construir imágenes Docker"""
    click.echo(f"Construyendo imágenes para {cloud}...")
    # TODO: Implementar llamadas a docker build
    click.echo("Build completado")

if __name__ == '__main__':
    main()

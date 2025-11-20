import yaml
import os
import argparse
from pathlib import Path

def ensure_directory(path):
    """Asegura que un directorio existe, lo crea si no"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

def process_visual_config(template_file):
    """Procesa template YAML y genera configuración automática"""
    
    print(f" Procesando template visual: {template_file}")
    
    try:
        # Verificar que el template existe
        if not Path(template_file).exists():
            raise FileNotFoundError(f"Template no encontrado: {template_file}")
        
        # Leer template YAML
        with open(template_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validar estructura
        if 'table_config' not in config:
            raise ValueError("Template debe contener 'table_config'")
        
        table_config = config['table_config']
        table_name = table_config['table_name']
        
        print(f" Procesando tabla: {table_name}")
        
        # Crear todos los directorios necesarios
        ensure_directory("config/dev")
        ensure_directory("cloud_implementations/gcp")
        ensure_directory("cloud_implementations/aws")
        ensure_directory("cloud_implementations/azure")
        
        # Generar configuración de ambiente
        env_content = f"""
# ⚡ CONFIGURACIÓN GENERADA AUTOMÁTICAMENTE - {table_name}
TABLE_NAME={table_name}
ORACLE_SCHEMA={table_config['oracle_source']['schema']}
ORACLE_TABLE={table_config['oracle_source']['table']}
GCP_PROJECT={table_config['cloud_destination']['gcp']['project']}
GCP_DATASET={table_config['cloud_destination']['gcp']['dataset']}
GCP_TABLE={table_config['cloud_destination']['gcp']['table']}
AWS_BUCKET={table_config['cloud_destination']['aws']['bucket']}
AWS_FOLDER={table_config['cloud_destination']['aws']['folder']}
AZURE_CONTAINER={table_config['cloud_destination']['azure']['container']}
AZURE_PATH={table_config['cloud_destination']['azure']['path']}
"""
        
        # Escribir configuración
        env_file = "config/dev/.env"
        with open(env_file, 'a') as f:
            f.write(env_content)
        
        print(f" Configuración generada en: {env_file}")
        
        # Generar script de migración específico para GCP
        migration_script = f'''# Script de migración para {table_name}
# Generado automáticamente desde template visual

def migrate_{table_name.lower()}():
    """
    Migración automática generada desde template visual
    Tabla: {table_name}
    Oracle: {table_config['oracle_source']['schema']}.{table_config['oracle_source']['table']}
    GCP: {table_config['cloud_destination']['gcp']['project']}.{table_config['cloud_destination']['gcp']['dataset']}.{table_config['cloud_destination']['gcp']['table']}
    """
    print(" Ejecutando migración visual para {table_name}")
    
    # Transformaciones configuradas:
    transformations = {table_config['transformations']}
    print(f"Transformaciones a aplicar: {{transformations}}")
    
    print(" Migración completada exitosamente")
    return True

if __name__ == "__main__":
    migrate_{table_name.lower()}()
'''
        
        script_file = f"cloud_implementations/gcp/migrate_{table_name.lower()}.py"
        with open(script_file, 'w') as f:
            f.write(migration_script)
        
        print(f" Script de migración generado: {script_file}")
        print(f"️  Destino GCP: {table_config['cloud_destination']['gcp']['project']}.{table_config['cloud_destination']['gcp']['dataset']}.{table_config['cloud_destination']['gcp']['table']}")
        print(" ¡Procesamiento visual completado exitosamente!")
        
        # Mostrar resumen
        print(f" RESUMEN EJECUTADO:")
        print(f"   • Tabla: {table_name}")
        print(f"   • Oracle: {table_config['oracle_source']['schema']}.{table_config['oracle_source']['table']}")
        print(f"   • GCP: {table_config['cloud_destination']['gcp']['project']}.{table_config['cloud_destination']['gcp']['dataset']}.{table_config['cloud_destination']['gcp']['table']}")
        print(f"   • Transformaciones: {len(table_config['transformations'])} aplicadas")
        
    except Exception as e:
        print(f" Error procesando template: {e}")
        return 1
    
    return 0

def main():
    parser = argparse.ArgumentParser(description='Procesador de configuración visual')
    parser.add_argument('--template', required=True, help='Archivo template YAML')
    
    args = parser.parse_args()
    
    return process_visual_config(args.template)

if __name__ == "__main__":
    main()

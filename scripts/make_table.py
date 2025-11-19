#!/usr/bin/env python3
"""
ORQUESTADOR PARA GENERADORES EXISTENTES + SISTEMA MULTICLOUD
"""

import os
import sys
import json
import argparse
from pathlib import Path

def load_tables_config():
    """Carga la configuracion maestra"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("tables_config", "template/tables_to_process.py")
        tables_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tables_config)
        return tables_config.TABLES_TO_PROCESS
    except Exception as e:
        print(f"ERROR: No se pudo cargar tables_to_process.py: {e}")
        return []

def run_table_generator(table_config):
    """Ejecuta tu table-generator existente"""
    table_name = table_config.get('oracle_table', 'unknown')
    print(f"  - Ejecutando table-generator para: {table_name}")
    
    # Aqui integrarias con tu table-generator existente
    table_gen_path = Path("generators/table-generator")
    if table_gen_path.exists():
        # Ejemplo de integracion - ajustar segun tu implementacion
        print(f"    - Table-generator encontrado en: {table_gen_path}")
        # os.system(f"python generators/table-generator/generate.py --table {table_name}")

def run_schema_generator(table_config):
    """Ejecuta tu schema-generator existente"""
    table_name = table_config.get('oracle_table', 'unknown')
    print(f"  - Ejecutando schema-generator para: {table_name}")
    
    schema_gen_path = Path("generators/schema-generator/schema_generator.py")
    if schema_gen_path.exists():
        print(f"    - Schema-generator encontrado: {schema_gen_path}")
        # Importar y usar tu schema generator existente
        try:
            sys.path.append('generators/schema-generator')
            from schema_generator import generate_schema
            # generate_schema(table_config)  # Ajustar segun tu funcion
        except ImportError as e:
            print(f"    - Error importando schema generator: {e}")

def run_dag_generator(table_config):
    """Ejecuta tu dag-generator existente"""
    table_name = table_config.get('oracle_table', 'unknown')
    print(f"  - Ejecutando dag-generator para: {table_name}")
    
    dag_gen_path = Path("generators/dag-generator")
    if dag_gen_path.exists():
        print(f"    - DAG-generator encontrado en: {dag_gen_path}")
        # Integrar con tu DAG generator

def run_procedure_generator(table_config):
    """Ejecuta tu procedure-generator existente"""
    table_name = table_config.get('oracle_table', 'unknown')
    print(f"  - Ejecutando procedure-generator para: {table_name}")
    
    proc_gen_path = Path("generators/procedure-generator")
    if proc_gen_path.exists():
        print(f"    - Procedure-generator encontrado en: {proc_gen_path}")

def generate_cloud_resources(table_config):
    """Genera recursos cloud-specific (nuestro sistema)"""
    table_name = table_config.get('oracle_table', 'unknown')
    
    # Obtener configuracion cloud
    cloud_config = table_config.get('cloud_provider', 'aws')
    
    if cloud_config == 'aws':
        print(f"  - Generando recursos AWS para: {table_name}")
        generate_aws_dag(table_config)
    elif cloud_config == 'azure':
        print(f"  - Generando recursos Azure para: {table_name}")
        generate_azure_dag(table_config)
    else:
        print(f"  - Generando recursos GCP para: {table_name}")

def generate_aws_dag(table_config):
    """Genera DAG para AWS usando templates"""
    table_name = table_config.get('oracle_table', 'unknown').lower()
    
    template_path = Path("clouds/aws/templates/dag_template.py")
    if template_path.exists():
        with open(template_path, 'r') as f:
            template = f.read()
        
        dag_content = template.replace('{table_name}', table_name)
        
        aws_dag_dir = Path("clouds/aws/dags")
        aws_dag_dir.mkdir(parents=True, exist_ok=True)
        
        dag_file = aws_dag_dir / f"dag_aws_{table_name}.py"
        with open(dag_file, 'w') as f:
            f.write(dag_content)
        print(f"    - DAG AWS generado: {dag_file}")

def generate_azure_dag(table_config):
    """Genera DAG para Azure usando templates"""
    table_name = table_config.get('oracle_table', 'unknown').lower()
    
    template_path = Path("clouds/azure/templates/dag_template.py")
    if template_path.exists():
        with open(template_path, 'r') as f:
            template = f.read()
        
        dag_content = template.replace('{table_name}', table_name)
        
        azure_dag_dir = Path("clouds/azure/dags")
        azure_dag_dir.mkdir(parents=True, exist_ok=True)
        
        dag_file = azure_dag_dir / f"dag_azure_{table_name}.py"
        with open(dag_file, 'w') as f:
            f.write(dag_content)
        print(f"    - DAG Azure generado: {dag_file}")

def update_all_tables():
    """Orquesta todos los generadores"""
    print("Iniciando generacion con orquestador integrado...")
    
    tables_config = load_tables_config()
    if not tables_config:
        print("No se encontraron tablas para procesar")
        return False
    
    print(f"Se encontraron {len(tables_config)} tablas")
    
    for table_config in tables_config:
        table_name = table_config.get('oracle_table', 'UNKNOWN')
        print(f"\n🎯 Procesando tabla: {table_name}")
        
        # 1. Usar tus generadores existentes
        run_table_generator(table_config)
        run_schema_generator(table_config)
        run_dag_generator(table_config)
        run_procedure_generator(table_config)
        
        # 2. Generar recursos cloud (nuestro sistema)
        generate_cloud_resources(table_config)
    
    print(f"\n✅ Generacion completada para {len(tables_config)} tablas")
    print("💡 Sistema integrado: Generadores existentes + Cloud resources")
    return True

def main():
    parser = argparse.ArgumentParser(description='Orquestador de generadores')
    parser.add_argument('--update-all', action='store_true', help='Generar todo')
    parser.add_argument('--table', type=str, help='Tabla especifica')
    
    args = parser.parse_args()
    
    if args.update_all:
        success = update_all_tables()
        exit(0 if success else 1)
    else:
        print("""
ORQUESTADOR DE GENERADORES - USO:
    python scripts/make_table.py --update-all

INTEGRACION:
    - Usa tus generadores Cookiecutter existentes
    - Agrega recursos cloud-specific
    - Configuracion centralizada en template/tables_to_process.py
        """)
        return True

if __name__ == "__main__":
    main()
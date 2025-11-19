#!/usr/bin/env python3
"""
SCRIPT PRINCIPAL PARA AUTOMATIZAR CONFIGURACIONES DE TABLAS

Este script lee la configuracion maestra desde template/tables_to_process.py
y genera automaticamente todos los archivos necesarios para cada tabla.

USO:
    python scripts/make_table.py --update-all    # Actualiza todas las tablas
    python scripts/make_table.py --table nombre_tabla  # Actualiza tabla especifica
"""

import os
import json
import argparse
from pathlib import Path

def load_tables_config():
    """Carga la configuracion maestra desde tables_to_process.py"""
    try:
        # Importar dinamicamente el archivo de configuracion
        import importlib.util
        spec = importlib.util.spec_from_file_location("tables_config", "template/tables_to_process.py")
        tables_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tables_config)
        
        print(f"Se encontraron {len(tables_config.TABLES_TO_PROCESS)} tablas para procesar:")
        for table in tables_config.TABLES_TO_PROCESS:
            print(f"  - {table.get('oracle_table', 'SIN_NOMBRE')}")
        
        return tables_config.TABLES_TO_PROCESS
    except Exception as e:
        print(f"ERROR: No se pudo cargar tables_to_process.py: {e}")
        return []

def generate_extraction_sql(table_config):
    """
    Genera archivo SQL para extraccion de datos desde la base origen
    CAMBIAR: Los nombres de campos y tabla segun tu estructura real
    """
    table_name = table_config.get('oracle_table', 'TABLA_EJEMPLO')
    schema_name = table_config.get('oracle_schema', 'ESQUEMA_ORIGEN')
    
    extraction_dir = Path("oracle")
    extraction_dir.mkdir(exist_ok=True)
    
    # PLANTILLA DE EXTRACCION - MODIFICAR CAMPOS SEGUN NECESIDAD
    sql_content = f"""-- Script de extraccion para tabla: {table_name}
-- AUTOGENERADO - NO MODIFICAR MANUALMENTE
-- Campos ficticios - REEMPLAZAR con la estructura real de tu tabla

SELECT
    ID_REGISTRO,                    -- CAMBIAR: Campo identificador unico
    CODIGO_TRANSACCION,             -- CAMBIAR: Codigo de transaccion
    TIPO_CANAL,                     -- CAMBIAR: Tipo de canal (ej: web, movil, sucursal)
    SISTEMA_ORIGEN,                 -- CAMBIAR: Sistema que origina el dato
    CODIGO_PRODUCTO,                -- CAMBIAR: Codigo del producto
    NUMERO_CLIENTE,                 -- CAMBIAR: Numero/RUT del cliente
    DIGITO_VERIFICADOR,             -- CAMBIAR: Digito verificador
    NUMERO_OPERACION,               -- CAMBIAR: Numero de operacion/contrato
    MONTO_OPERACION,                -- CAMBIAR: Monto de la operacion
    TO_CHAR(FECHA_SOLICITUD, 'YYYY-MM-DD HH24:MI:SS') AS FECHA_SOLICITUD,  -- CAMBIAR: Fecha de solicitud
    USUARIO_SOLICITANTE,            -- CAMBIAR: Usuario que realiza la solicitud
    EMAIL_NOTIFICACION,             -- CAMBIAR: Email para notificaciones
    CODIGO_RESPUESTA,               -- CAMBIAR: Codigo de respuesta del sistema
    ID_APLICACION,                  -- CAMBIAR: ID de aplicacion externa
    CODIGO_RESPUESTA_EXT,           -- CAMBIAR: Codigo respuesta externa
    DESCRIPCION_RESPUESTA,          -- CAMBIAR: Descripcion de la respuesta
    TO_CHAR(FECHA_RESPUESTA, 'YYYY-MM-DD HH24:MI:SS') AS FECHA_RESPUESTA,  -- CAMBIAR: Fecha de respuesta
    NUMERO_REINTENTOS,              -- CAMBIAR: Numero de reintentos
    ESTADO_OPERACION                -- CAMBIAR: Estado de la operacion
FROM
    {schema_name}.{table_name}      -- CAMBIAR: Schema y nombre de tabla real
"""
    
    file_name = f"{table_name.lower()}.sql"
    file_path = extraction_dir / file_name
    with open(file_path, 'w') as f:
        f.write(sql_content)
    print(f"  - SQL de extraccion generado: {file_path}")

def generate_staging_table_sql(table_config):
    """
    Genera SQL para crear tabla de staging en BigQuery
    CAMBIAR: Los tipos de datos y nombres de campos segun necesidad
    """
    table_name = table_config.get('oracle_table', 'tabla_ejemplo').lower()
    staging_dir = Path("sql/create_table")
    staging_dir.mkdir(parents=True, exist_ok=True)
    
    sql_content = f"""-- Tabla de staging para: {table_name}
-- AUTOGENERADO - Campos ficticios, REEMPLAZAR con estructura real

DECLARE table_exists BOOL;

SET table_exists = (
  SELECT COUNT(1) > 0
  FROM `${{PROJECT_NAME}}.staging_dataset.INFORMATION_SCHEMA.TABLES`
  WHERE table_name = 'stg_{table_name}'
);

IF NOT table_exists THEN
  CREATE TABLE `${{PROJECT_NAME}}.staging_dataset.stg_{table_name}` (
    -- CAMBIAR: Definir la estructura real de campos aqui
    id_registro NUMERIC,                    -- CAMBIAR: Tipo y nombre real
    codigo_transaccion STRING,              -- CAMBIAR: Tipo y nombre real
    tipo_canal INTEGER,                     -- CAMBIAR: Tipo y nombre real
    sistema_origen INTEGER,                 -- CAMBIAR: Tipo y nombre real
    codigo_producto INTEGER,                -- CAMBIAR: Tipo y nombre real
    numero_cliente NUMERIC,                 -- CAMBIAR: Tipo y nombre real
    digito_verificador STRING,              -- CAMBIAR: Tipo y nombre real
    numero_operacion NUMERIC,               -- CAMBIAR: Tipo y nombre real
    monto_operacion NUMERIC,                -- CAMBIAR: Tipo y nombre real
    fecha_solicitud DATETIME,               -- CAMBIAR: Tipo y nombre real
    usuario_solicitante STRING,             -- CAMBIAR: Tipo y nombre real
    email_notificacion STRING,              -- CAMBIAR: Tipo y nombre real
    codigo_respuesta INTEGER,               -- CAMBIAR: Tipo y nombre real
    id_aplicacion NUMERIC,                  -- CAMBIAR: Tipo y nombre real
    codigo_respuesta_ext STRING,            -- CAMBIAR: Tipo y nombre real
    descripcion_respuesta STRING,           -- CAMBIAR: Tipo y nombre real
    fecha_respuesta DATETIME,               -- CAMBIAR: Tipo y nombre real
    numero_reintentos INTEGER,              -- CAMBIAR: Tipo y nombre real
    estado_operacion INTEGER,               -- CAMBIAR: Tipo y nombre real
    
    -- Campos de auditoria (opcionales)
    fecha_creacion DATETIME DEFAULT CURRENT_DATETIME(),
    fecha_actualizacion DATETIME DEFAULT CURRENT_DATETIME()
  );
END IF
"""
    
    file_path = staging_dir / f"stg_{table_name}.sql"
    with open(file_path, 'w') as f:
        f.write(sql_content)
    print(f"  - SQL de staging generado: {file_path}")

def generate_destination_table_sql(table_config):
    """
    Genera SQL para crear tabla destino final en BigQuery
    CAMBIAR: Estrategia de particion y clustering segun necesidades
    """
    table_name = table_config.get('oracle_table', 'tabla_ejemplo').lower()
    dataset = table_config.get('dataset_destino', 'dataset_destino_ejemplo')
    destination_dir = Path("sql/create_table")
    destination_dir.mkdir(parents=True, exist_ok=True)
    
    sql_content = f"""-- Tabla destino para: {table_name}
-- AUTOGENERADO - Ajustar particion y clustering segun necesidades

DECLARE table_exists BOOL;
DECLARE primary_key_exists BOOL;

SET table_exists = (
  SELECT COUNT(1) > 0
  FROM `${{PROJECT_NAME}}.{dataset}.INFORMATION_SCHEMA.TABLES`
  WHERE table_name = 'dep_{table_name}'
);

SET primary_key_exists = (
  SELECT COUNT(1) > 0
  FROM `${{PROJECT_NAME}}.{dataset}.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_name = 'dep_{table_name}' AND column_name IN ("id_registro")
);

IF NOT table_exists THEN
  CREATE TABLE `${{PROJECT_NAME}}.{dataset}.dep_{table_name}` (
    -- CAMBIAR: Estructura de campos reales
    id_registro NUMERIC,
    codigo_transaccion STRING,
    tipo_canal INTEGER,
    sistema_origen INTEGER,
    codigo_producto INTEGER,
    numero_cliente NUMERIC,
    digito_verificador STRING,
    numero_operacion NUMERIC,
    monto_operacion NUMERIC,
    fecha_solicitud DATETIME,
    usuario_solicitante STRING,
    email_notificacion STRING,
    codigo_respuesta INTEGER,
    id_aplicacion NUMERIC,
    codigo_respuesta_ext STRING,
    descripcion_respuesta STRING,
    fecha_respuesta DATETIME,
    numero_reintentos INTEGER,
    estado_operacion INTEGER,
    fecha_creacion DATETIME DEFAULT NULL,
    fecha_actualizacion DATETIME DEFAULT NULL
  )
  -- CAMBIAR: Estrategia de particion (usar campo de fecha apropiado)
  PARTITION BY DATETIME_TRUNC(fecha_respuesta, DAY)
  -- CAMBIAR: Campos de clustering segun patrones de consulta
  CLUSTER BY tipo_canal, codigo_producto
  OPTIONS(
    labels=[
      ('origen', '{table_config.get('origen', 'origen_desconocido')}'), 
      ('ambiente', '{table_config.get('entorno', 'dev')}'),
      ('producto', '{table_config.get('producto', 'producto_ejemplo')}')
    ]
  );
END IF;

IF NOT primary_key_exists THEN
  -- CAMBIAR: Campo de llave primaria real
  ALTER TABLE `${{PROJECT_NAME}}.{dataset}.dep_{table_name}`
  ADD PRIMARY KEY (id_registro) NOT ENFORCED;
END IF
"""
    
    file_path = destination_dir / f"dep_{table_name}.sql"
    with open(file_path, 'w') as f:
        f.write(sql_content)
    print(f"  - SQL de destino generado: {file_path}")

def generate_json_config(table_config):
    """
    Genera archivo de configuracion JSON para la tabla
    CAMBIAR: Configuracion de particion y clustering segun necesidades
    """
    table_name = table_config.get('oracle_table', 'TABLA_EJEMPLO')
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    config_data = {
        "table_name": table_name,
        # CAMBIAR: Campo de particion apropiado para tus datos
        "partition_field": "fecha_respuesta",
        "partition_data_type": "DATETIME",
        # CAMBIAR: Campos de clustering segun patrones de consulta
        "clustering_fields": ["tipo_canal", "codigo_producto"],
        "date_field_type": "DATETIME",
        "dataset": table_config.get('dataset_destino', 'dataset_destino_ejemplo'),
        "labels": [
            {"key": "origen", "value": table_config.get('origen', 'origen_desconocido')},
            {"key": "ambiente", "value": table_config.get('entorno', 'dev')},
            {"key": "producto", "value": table_config.get('producto', 'producto_ejemplo')},
            {"key": "dominio", "value": table_config.get('dominio', 'dominio_ejemplo')}
        ]
    }
    
    file_path = config_dir / f"{table_name.lower()}.json"
    with open(file_path, 'w') as f:
        json.dump(config_data, f, indent=2)
    print(f"  - Config JSON generado: {file_path}")

def generate_aws_resources(table_config):
    """Genera recursos especificos para AWS"""
    table_name = table_config.get('oracle_table', 'tabla_ejemplo').lower()
    
    # Cargar template de DAG AWS
    template_path = Path("clouds/aws/templates/dag_template.py")
    if template_path.exists():
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Reemplazar placeholders
        dag_content = template_content.replace('{table_name}', table_name)
        dag_content = dag_content.replace('{s3_ingest_path}', table_config.get('gcs_ingest_path', 'ingest/path'))
        dag_content = dag_content.replace('{redshift_schema}', table_config.get('dataset_destino', 'schema_ejemplo'))
        
        # Guardar DAG generado
        aws_dag_dir = Path("clouds/aws/dags")
        aws_dag_dir.mkdir(parents=True, exist_ok=True)
        
        dag_file = aws_dag_dir / f"dag_aws_{table_name}.py"
        with open(dag_file, 'w') as f:
            f.write(dag_content)
        print(f"  - DAG AWS generado: {dag_file}")

def generate_azure_resources(table_config):
    """Genera recursos especificos para Azure"""
    table_name = table_config.get('oracle_table', 'tabla_ejemplo').lower()
    
    # Cargar template de DAG Azure
    template_path = Path("clouds/azure/templates/dag_template.py")
    if template_path.exists():
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Reemplazar placeholders
        dag_content = template_content.replace('{table_name}', table_name)
        dag_content = dag_content.replace('{adls_path}', table_config.get('gcs_ingest_path', 'ingest/path'))
        
        # Guardar DAG generado
        azure_dag_dir = Path("clouds/azure/dags")
        azure_dag_dir.mkdir(parents=True, exist_ok=True)
        
        dag_file = azure_dag_dir / f"dag_azure_{table_name}.py"
        with open(dag_file, 'w') as f:
            f.write(dag_content)
        print(f"  - DAG Azure generado: {dag_file}")

# AQUI VA LA FUNCION QUE ME MOSTRASTE
def update_all_tables():
    """Actualiza todas las tablas basado en la configuracion maestra"""
    print("Iniciando actualizacion de tablas...")
    
    tables_config = load_tables_config()
    if not tables_config:
        print("No se encontraron tablas para procesar")
        return False
    
    for table_config in tables_config:
        table_name = table_config.get('oracle_table', 'TABLA_DESCONOCIDA')
        print(f"\nProcesando tabla: {table_name}")
        
        # Generar todos los archivos para esta tabla
        generate_extraction_sql(table_config)
        generate_staging_table_sql(table_config)
        generate_destination_table_sql(table_config)
        generate_json_config(table_config)
        
        # Generar recursos para clouds
        generate_aws_resources(table_config)
        generate_azure_resources(table_config)
    
    print(f"\nActualizacion completada para {len(tables_config)} tablas")
    return True

def update_single_table(table_name):
    """Actualiza una tabla especifica"""
    print(f"Buscando tabla: {table_name}")
    
    tables_config = load_tables_config()
    if not tables_config:
        print("No se encontraron tablas para procesar")
        return False
    
    # Buscar la tabla especifica
    table_config = None
    for table in tables_config:
        if table.get('oracle_table', '').lower() == table_name.lower():
            table_config = table
            break
    
    if not table_config:
        print(f"ERROR: Tabla '{table_name}' no encontrada en la configuracion")
        return False
    
    print(f"Procesando tabla especifica: {table_name}")
    generate_extraction_sql(table_config)
    generate_staging_table_sql(table_config)
    generate_destination_table_sql(table_config)
    generate_json_config(table_config)
    generate_aws_resources(table_config)
    generate_azure_resources(table_config)
    
    print(f"Actualizacion completada para tabla: {table_name}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Generar configuraciones de tablas automaticamente')
    parser.add_argument('--update-all', action='store_true', 
                       help='Actualizar todas las tablas definidas en tables_to_process.py')
    parser.add_argument('--table', type=str,
                       help='Actualizar una tabla especifica por nombre')
    
    args = parser.parse_args()
    
    if args.update_all:
        success = update_all_tables()
        exit(0 if success else 1)
    elif args.table:
        success = update_single_table(args.table)
        exit(0 if success else 1)
    else:
        print("""
OPCIONES DE USO:
    python scripts/make_table.py --update-all    # Actualiza TODAS las tablas
    python scripts/make_table.py --table nombre  # Actualiza tabla ESPECIFICA

CONFIGURACION:
    Editar template/tables_to_process.py para agregar/modificar tablas
        """)
        return True

if __name__ == "__main__":
    main()
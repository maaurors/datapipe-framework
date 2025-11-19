"""
TEMPLATE DE DAG PARA AWS - AUTOGENERADO

INSTRUCCIONES:
1. Reemplazar los nombres de campos ficticios con la estructura real
2. Ajustar las conexiones segun tu entorno AWS
3. Configurar los paths de S3 apropiados
"""

AWS_DAG_TEMPLATE = '''
from airflow import DAG
from airflow.providers.amazon.aws.operators.redshift import RedshiftSQLOperator
from airflow.providers.amazon.aws.transfers.oracle_to_s3 import OracleToS3Operator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from datetime import datetime

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 2
}

with DAG(
    "dag_aws_{table_name}",
    default_args=default_args,
    schedule_interval="@daily",
    tags=["aws", "oracle", "redshift"]
) as dag:

    # TAREA 1: Extraer datos de Oracle a S3
    extract_to_s3 = OracleToS3Operator(
        task_id="extract_{table_name}_to_s3",
        oracle_conn_id="oracle_conn",  # CAMBIAR: ID de conexion Oracle en Airflow
        s3_bucket="{{ dag_run.conf['s3_bucket'] }}",  # CAMBIAR: Bucket S3 destino
        s3_key="{s3_ingest_path}/{table_name}/",  # CAMBIAR: Path en S3
        sql_query="sql/oracle/{table_name}.sql",  # Usa el SQL generado automaticamente
        file_format="PARQUET"  # CAMBIAR: Formato de archivo (PARQUET, CSV, JSON)
    )

    # TAREA 2: Cargar datos de S3 a Redshift
    load_to_redshift = S3ToRedshiftOperator(
        task_id="load_{table_name}_to_redshift",
        s3_bucket="{{ dag_run.conf['s3_bucket'] }}",
        s3_key="{s3_ingest_path}/{table_name}/*.parquet",
        redshift_conn_id="redshift_conn",  # CAMBIAR: ID de conexion Redshift
        schema="{redshift_schema}",  # CAMBIAR: Schema en Redshift
        table="{table_name}",  # CAMBIAR: Nombre de tabla en Redshift
        copy_options=["FORMAT AS PARQUET"]  # CAMBIAR: Opciones de carga
    )

    # TAREA 3: Transformaciones en Redshift (opcional)
    transform_data = RedshiftSQLOperator(
        task_id="transform_{table_name}",
        redshift_conn_id="redshift_conn",
        sql="sql/procedures/sp_merge_{table_name}.sql"  # CAMBIAR: SQL de transformacion
    )

    # DEFINIR DEPENDENCIAS
    extract_to_s3 >> load_to_redshift >> transform_data
'''

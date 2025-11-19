"""
TEMPLATE DE DAG PARA AZURE - AUTOGENERADO

INSTRUCCIONES:
1. Reemplazar los nombres de campos ficticios con la estructura real
2. Ajustar las conexiones segun tu entorno Azure
3. Configurar los paths de ADLS apropiados
"""

AZURE_DAG_TEMPLATE = '''
from airflow import DAG
from airflow.providers.microsoft.azure.operators.synapse import AzureSynapseRunPipelineOperator
from airflow.providers.microsoft.azure.transfers.oracle_to_azure_data_lake import OracleToAzureDataLakeStorageOperator
from datetime import datetime

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 2
}

with DAG(
    "dag_azure_tpp_recarga",
    default_args=default_args,
    schedule_interval="@daily",
    tags=["azure", "oracle", "synapse"]
) as dag:

    # TAREA 1: Extraer datos de Oracle a Azure Data Lake
    extract_to_adls = OracleToAzureDataLakeStorageOperator(
        task_id="extract_tpp_recarga_to_adls",
        oracle_conn_id="oracle_conn",  # CAMBIAR: ID de conexion Oracle
        container_name="{{ dag_run.conf[''adls_container''] }}",  # CAMBIAR: Contenedor ADLS
        blob_name="data_ingest_proybd/de_apoyo/filiales/tapp/migracion_tapp/analitico/tpp_recarga/data.parquet",  # CAMBIAR: Path en ADLS
        sql_query="sql/oracle/tpp_recarga.sql"  # Usa el SQL generado automaticamente
    )

    # TAREA 2: Ejecutar pipeline en Azure Synapse
    load_to_synapse = AzureSynapseRunPipelineOperator(
        task_id="load_tpp_recarga_to_synapse",
        azure_synapse_conn_id="synapse_conn",  # CAMBIAR: ID de conexion Synapse
        pipeline_name="load_tpp_recarga_pipeline",  # CAMBIAR: Nombre del pipeline
        parameters={{"table_name": "tpp_recarga"}}  # CAMBIAR: Parametros del pipeline
    )

    # DEFINIR DEPENDENCIAS
    extract_to_adls >> load_to_synapse
'''
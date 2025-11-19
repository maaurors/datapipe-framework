"""
CONFIGURACION MAESTRA - SISTEMA INTEGRADO
"""

TABLES_TO_PROCESS = [
    {
        'oracle_table': 'TPP_RECARGA',
        'bigquery_table': 'tpp_recarga', 
        'dataset_destino': 'dep_de_apoyo_filiales_tapp',
        'origen': 'proybd',
        'load_mode': 'full',
        'oracle_schema': 'TPP',
        
        # CONFIGURACION CLOUD - CAMBIAR AQUI
        'cloud_provider': 'aws',  # 'aws', 'azure', 'gcp'
        
        'aws_config': {
            'redshift_schema': 'dep_de_apoyo_filiales_tapp',
            's3_ingest_path': 'data_ingest/aws/tpp_recarga'
        }
    }
]
"""
CONFIGURACION MAESTRA DE TABLAS - ARCHIVO PRINCIPAL

INSTRUCCIONES:
1. Agregar nuevas tablas en la lista TABLES_TO_PROCESS
2. Ejecutar: python scripts/make_table.py --update-all
3. El sistema generara automaticamente todos los archivos necesarios

CAMBIOS REQUERIDOS POR EL USUARIO:
- Reemplazar nombres de campos ficticios con estructura real
- Ajustar tipos de datos segun necesidad
- Definir estrategias de particion y clustering apropiadas
"""

TABLES_TO_PROCESS = [
    {
        # INFORMACION BASICA REQUERIDA
        'oracle_table': 'TPP_RECARGA',                    # CAMBIAR: Nombre real en Oracle
        'bigquery_table': 'tpp_recarga',                  # CAMBIAR: Nombre en BigQuery
        'dataset_destino': 'dep_de_apoyo_filiales_tapp',  # CAMBIAR: Dataset destino
        'origen': 'proybd',                               # CAMBIAR: Origen de datos
        
        # CONFIGURACION OPCIONAL
        'load_mode': 'full',                              # full o incremental
        'oracle_schema': 'TPP',                           # CAMBIAR: Schema Oracle
        'dominio': 'de_apoyo',
        'subdominio': 'filiales/tapp',
        'producto': 'migracion_tapp',
        'entorno': 'analitico',
        
        # RUTAS (se auto-completaran)
        'store_procedure': 'sp_merge_dep_tpp_recarga',
        'gcs_schema_avsc_path': 'de_apoyo/filiales/tapp/migracion_tapp/proybd/analitico',
        'gcs_schema_json_path': 'de_apoyo/filiales/tapp/migracion_tapp/proybd/analitico',
        'gcs_query': 'de_apoyo/filiales/tapp/migracion_tapp/proybd/analitico',
        'gcs_ingest_path': 'data_ingest_proybd/de_apoyo/filiales/tapp/migracion_tapp/analitico',
        'gcs_raw_path': 'de_apoyo/filiales/tapp/migracion_tapp/proybd/analitico'
    },
    # EJEMPLO DE NUEVA TABLA - DESCOMENTAR Y MODIFICAR
    # {
    #     'oracle_table': 'MI_NUEVA_TABLA',
    #     'bigquery_table': 'mi_nueva_tabla',
    #     'dataset_destino': 'mi_dataset',
    #     'origen': 'mi_origen',
    #     'load_mode': 'full',
    #     'oracle_schema': 'MI_ESQUEMA'
    # }
]
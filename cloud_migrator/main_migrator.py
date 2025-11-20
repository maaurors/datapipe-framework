import argparse

# Configuración simple por ambiente
CONFIG = {
    'dev': {
        'oracle_host': 'oracle-dev.company.com',
        'gcp_project': 'my-project-dev',
        'aws_region': 'us-east-1',
        'log_level': 'DEBUG'
    },
    'qa': {
        'oracle_host': 'oracle-qa.company.com', 
        'gcp_project': 'my-project-qa',
        'aws_region': 'us-east-1',
        'log_level': 'INFO'
    },
    'prd': {
        'oracle_host': 'oracle-prd.company.com',
        'gcp_project': 'my-project-prd', 
        'aws_region': 'us-east-1',
        'log_level': 'WARNING'
    }
}

def main():
    parser = argparse.ArgumentParser(description='Cloud Data Migrator')
    parser.add_argument('--cloud', required=True, choices=['gcp','aws','azure'])
    parser.add_argument('--table', required=True, help='Nombre de la tabla a migrar')
    parser.add_argument('--env', required=True, choices=['dev','qa','prd'], help='Ambiente')
    parser.add_argument('--execution-mode', choices=['local','cloud'], default='local', help='Modo de ejecución')
    
    args = parser.parse_args()
    
    # Cargar configuración del ambiente
    config = CONFIG[args.env]
    
    print(f" Configuración para ambiente: {args.env}")
    print(f"️  Cloud: {args.cloud.upper()}")
    print(f" Tabla: {args.table}")
    print(f" Modo: {args.execution_mode}")
    
    try:
        # Importar según el cloud seleccionado
        if args.cloud == 'gcp':
            from cloud_implementations.gcp.dataflow_migrator import GCPDataflowMigrator
            migrator = GCPDataflowMigrator(config)
            if args.execution_mode == 'cloud':
                migrator.run_dataflow_job(args.table, f"{config['gcp_project']}.dataset.{args.table}")
            else:
                migrator.migrate(args.table, f"local_test.{args.table}")
        
        elif args.cloud == 'aws':
            from cloud_implementations.aws.glue_migrator import AWSGlueMigrator
            migrator = AWSGlueMigrator(config)
            if args.execution_mode == 'cloud':
                migrator.run_glue_job(args.table, f"redshift_{args.table}")
            else:
                migrator.migrate(args.table, f"local_test.{args.table}")
        
        elif args.cloud == 'azure':
            print(" Implementación Azure en progreso...")
            # from cloud_implementations.azure.data_factory_migrator import AzureDataFactoryMigrator
            # migrator = AzureDataFactoryMigrator(config)
        
        print(" Proceso completado")
        
    except Exception as e:
        print(f" Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()

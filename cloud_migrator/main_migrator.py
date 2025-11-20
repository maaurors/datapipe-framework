import argparse

def main():
    print(" Cloud Migrator funcionando correctamente!")
    print("Prueba: python -m cloud_migrator.main_migrator --cloud gcp --table prueba")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--cloud', required=True, choices=['gcp','aws','azure'])
    parser.add_argument('--table', required=True)
    
    args = parser.parse_args()
    
    print(f" Configurado para migrar tabla '{args.table}' a {args.cloud.upper()}")

if __name__ == "__main__":
    main()

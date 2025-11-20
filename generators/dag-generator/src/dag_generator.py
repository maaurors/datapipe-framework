#!/usr/bin/env python3
"""Generic DAG Generator for DataPipe Framework"""

import argparse

class GenericDAGGenerator:
    def __init__(self, table_name: str = "", cloud: str = "gcp", load_mode: str = "incremental"):
        self.table_name = table_name
        self.cloud = cloud
        self.load_mode = load_mode
        
    def generate_dag(self) -> str:
        dag_name = f"dag_{self.table_name}"
        
        dag_code = f'from airflow import DAG\n'
        dag_code += f'from airflow.utils.dates import days_ago\n'
        dag_code += f'from airflow.providers.docker.operators.docker import DockerOperator\n'
        dag_code += f'from airflow.operators.dummy import DummyOperator\n'
        dag_code += f'\n'
        dag_code += f'default_args = {{\n'
        dag_code += f"    'start_date': days_ago(1),\n"
        dag_code += f"    'retries': 1,\n"
        dag_code += f'}}\n'
        dag_code += f'\n'
        dag_code += f'with DAG(\n'
        dag_code += f'    "{dag_name}",\n'
        dag_code += f'    default_args=default_args,\n'
        dag_code += f'    schedule_interval="@daily",\n'
        dag_code += f'    catchup=False,\n'
        dag_code += f'    tags=["datapipe", "{self.cloud}", "{self.load_mode}"]\n'
        dag_code += f') as dag:\n'
        dag_code += f'\n'
        dag_code += f'    start = DummyOperator(task_id="start")\n'
        dag_code += f'    \n'
        dag_code += f'    extract = DockerOperator(\n'
        dag_code += f'        task_id="extract",\n'
        dag_code += f'        image="datapipe/extractor-{self.cloud}:latest",\n'
        dag_code += f'        command="--table {self.table_name}",\n'
        dag_code += f'        docker_url="unix://var/run/docker.sock"\n'
        dag_code += f'    )\n'
        dag_code += f'    \n'
        dag_code += f'    load = DockerOperator(\n'
        dag_code += f'        task_id="load", \n'
        dag_code += f'        image="datapipe/loader-{self.cloud}:latest",\n'
        dag_code += f'        command="--table {self.table_name}",\n'
        dag_code += f'        docker_url="unix://var/run/docker.sock"\n'
        dag_code += f'    )\n'
        dag_code += f'    \n'
        dag_code += f'    end = DummyOperator(task_id="end")\n'
        dag_code += f'    \n'
        dag_code += f'    start >> extract >> load >> end\n'
        
        return dag_code

def main():
    parser = argparse.ArgumentParser(description='Generic DAG Generator')
    parser.add_argument('--table-name', type=str, help='Table name')
    parser.add_argument('--cloud', type=str, default='gcp', help='Cloud provider')
    parser.add_argument('--load-mode', type=str, default='incremental', help='Load mode')
    
    args = parser.parse_args()
    
    generator = GenericDAGGenerator(
        table_name=args.table_name or "generic_table",
        cloud=args.cloud,
        load_mode=args.load_mode
    )
    
    dag = generator.generate_dag()
    print("=== AIRFLOW DAG ===")
    print(dag)

if __name__ == "__main__":
    main()

.PHONY: help schemas tables procedures dag

PROJECT_NAME = {{cookiecutter.project_slug}}

help:
	@echo "Comandos disponibles:"
	@echo "  make schemas    - Generar schemas"
	@echo "  make tables     - Generar DDL"
	@echo "  make procedures - Generar stored procedures"
	@echo "  make dag        - Generar DAG"

schemas:
	@echo "Generando schemas..."
	docker run --rm \
		-v $(PWD)/config/schemas:/output \
		-e ORACLE_TABLE={{cookiecutter.oracle_table}} \
		datapipe/schema-generator:latest
	@echo "Ver: config/schemas/"

tables:
	@echo "Generando DDL..."
	@mkdir -p sql/create_tables
	@echo "CREATE TABLE {{cookiecutter.bigquery_dataset}}.{{cookiecutter.project_slug}} (" > sql/create_tables/{{cookiecutter.project_slug}}.sql
	@echo "  id INT64 NOT NULL," >> sql/create_tables/{{cookiecutter.project_slug}}.sql
	@echo "  name STRING" >> sql/create_tables/{{cookiecutter.project_slug}}.sql
	@echo ");" >> sql/create_tables/{{cookiecutter.project_slug}}.sql
	@echo "DDL generado en sql/create_tables/"

procedures:
	@echo "Generando procedures..."
	@mkdir -p sql/store_procedures
	@echo "-- Stored Procedure para {{cookiecutter.project_slug}}" > sql/store_procedures/sp_merge_{{cookiecutter.project_slug}}.sql
	@echo "Procedure generado en sql/store_procedures/"

dag:
	@echo "Generando DAG..."
	@mkdir -p dags
	@echo "# DAG generado para {{cookiecutter.project_slug}}" > dags/dag_{{cookiecutter.project_slug}}.py
	@echo "DAG generado en dags/"

.PHONY: help schemas tables procedures dag

PROJECT_NAME = tpp_recarga

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
		-e ORACLE_TABLE=tpp_recarga \
		datapipe/schema-generator:latest
	@echo "Ver: config/schemas/"

tables:
	@echo "Generando DDL..."
	@mkdir -p sql/create_tables
	@echo "CREATE TABLE tpp_recarga.tpp_recarga (" > sql/create_tables/tpp_recarga.sql
	@echo "  id INT64 NOT NULL," >> sql/create_tables/tpp_recarga.sql
	@echo "  name STRING" >> sql/create_tables/tpp_recarga.sql
	@echo ");" >> sql/create_tables/tpp_recarga.sql
	@echo "DDL generado en sql/create_tables/"

procedures:
	@echo "Generando procedures..."
	@mkdir -p sql/store_procedures
	@echo "-- Stored Procedure para tpp_recarga" > sql/store_procedures/sp_merge_tpp_recarga.sql
	@echo "Procedure generado en sql/store_procedures/"

dag:
	@echo "Generando DAG..."
	@mkdir -p dags
	@echo "# DAG generado para tpp_recarga" > dags/dag_tpp_recarga.py
	@echo "DAG generado en dags/"

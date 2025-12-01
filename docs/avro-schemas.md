# Schemas AVRO y Tipos de Datos

DataPipe utiliza **Apache AVRO** como formato intermedio estándar para todas las migraciones. Esto garantiza consistencia, compresión y evolución de esquemas.

## Mapeo de Tipos (Oracle → AVRO)

El generador de schemas (`datapipe generate schema`) realiza la siguiente conversión automática:

| Tipo Oracle | Tipo AVRO | Tipo Lógico | Notas |
|-------------|-----------|-------------|-------|
| VARCHAR2    | string    | -           | UTF-8 |
| NVARCHAR2   | string    | -           | UTF-8 |
| CHAR        | string    | -           | Trimmed |
| NUMBER      | double    | -           | Precisión doble |
| INTEGER     | long      | -           | 64-bit |
| DATE        | long      | timestamp-millis | Epoch ms |
| TIMESTAMP   | long      | timestamp-millis | Epoch ms |
| CLOB        | string    | -           | Manejo eficiente |
| BLOB        | bytes     | -           | Datos binarios |

## Schema Evolution

AVRO permite evolucionar el esquema de la tabla sin romper los pipelines existentes.

### Reglas de Compatibilidad

1. **Agregar campos**: Se debe proveer un valor `default`.
2. **Eliminar campos**: El campo eliminado debe tener un `default` en el esquema anterior.
3. **Cambiar tipos**: Solo si son compatibles (ej. `int` -> `long`).

### Ejemplo de Schema Generado

```json
{
  "type": "record",
  "name": "clientes",
  "namespace": "oracle.schema",
  "fields": [
    {
      "name": "id",
      "type": "long"
    },
    {
      "name": "nombre",
      "type": ["null", "string"],
      "default": null
    },
    {
      "name": "fecha_registro",
      "type": ["null", {"type": "long", "logicalType": "timestamp-millis"}],
      "default": null
    }
  ]
}
```

## Nullable Fields

Todos los campos que son `NULLABLE` en Oracle se convierten en una unión `["null", "type"]` en AVRO, permitiendo valores nulos explícitos.

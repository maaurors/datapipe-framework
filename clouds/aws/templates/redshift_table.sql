-- TEMPLATE DE TABLA REDSHIFT PARA {table_name}
-- AUTOGENERADO - AJUSTAR ESTRUCTURA SEGUN NECESIDAD

CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
    -- CAMBIAR: Estructura de campos reales
    id_registro NUMERIC,                    -- CAMBIAR: Tipo y nombre real
    codigo_transaccion VARCHAR(50),         -- CAMBIAR: Tipo y nombre real  
    tipo_canal INTEGER,                     -- CAMBIAR: Tipo y nombre real
    sistema_origen INTEGER,                 -- CAMBIAR: Tipo y nombre real
    codigo_producto INTEGER,                -- CAMBIAR: Tipo y nombre real
    numero_cliente NUMERIC,                 -- CAMBIAR: Tipo y nombre real
    digito_verificador VARCHAR(1),          -- CAMBIAR: Tipo y nombre real
    numero_operacion NUMERIC,               -- CAMBIAR: Tipo y nombre real
    monto_operacion NUMERIC,                -- CAMBIAR: Tipo y nombre real
    fecha_solicitud TIMESTAMP,              -- CAMBIAR: Tipo y nombre real
    usuario_solicitante VARCHAR(50),        -- CAMBIAR: Tipo y nombre real
    email_notificacion VARCHAR(100),        -- CAMBIAR: Tipo y nombre real
    codigo_respuesta INTEGER,               -- CAMBIAR: Tipo y nombre real
    id_aplicacion NUMERIC,                  -- CAMBIAR: Tipo y nombre real
    codigo_respuesta_ext VARCHAR(10),       -- CAMBIAR: Tipo y nombre real
    descripcion_respuesta VARCHAR(500),     -- CAMBIAR: Tipo y nombre real
    fecha_respuesta TIMESTAMP,              -- CAMBIAR: Tipo y nombre real
    numero_reintentos INTEGER,              -- CAMBIAR: Tipo y nombre real
    estado_operacion INTEGER,               -- CAMBIAR: Tipo y nombre real
    
    -- Campos de auditoria
    fecha_creacion TIMESTAMP DEFAULT GETDATE(),
    fecha_actualizacion TIMESTAMP DEFAULT GETDATE()
)
-- CAMBIAR: Estrategia de distribucion segun patrones de query
DISTKEY(id_registro)
-- CAMBIAR: Ordenamiento para optimizar consultas
SORTKEY(fecha_respuesta, tipo_canal);

-- COMENTARIOS PARA DOCUMENTACION
COMMENT ON TABLE {schema}.{table_name} IS 'Tabla para {table_name} - Cargada desde Oracle';
COMMENT ON COLUMN {schema}.{table_name}.id_registro IS 'Identificador unico del registro';
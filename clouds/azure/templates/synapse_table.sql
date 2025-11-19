-- TEMPLATE DE TABLA SYNAPSE PARA {table_name}
-- AUTOGENERADO - AJUSTAR ESTRUCTURA SEGUN NECESIDAD

CREATE TABLE {schema}.{table_name} (
    -- CAMBIAR: Estructura de campos reales
    id_registro NUMERIC,                    -- CAMBIAR: Tipo y nombre real
    codigo_transaccion NVARCHAR(50),        -- CAMBIAR: Tipo y nombre real
    tipo_canal INTEGER,                     -- CAMBIAR: Tipo y nombre real
    sistema_origen INTEGER,                 -- CAMBIAR: Tipo y nombre real
    codigo_producto INTEGER,                -- CAMBIAR: Tipo y nombre real
    numero_cliente NUMERIC,                 -- CAMBIAR: Tipo y nombre real
    digito_verificador NVARCHAR(1),         -- CAMBIAR: Tipo y nombre real
    numero_operacion NUMERIC,               -- CAMBIAR: Tipo y nombre real
    monto_operacion NUMERIC,                -- CAMBIAR: Tipo y nombre real
    fecha_solicitud DATETIME2,              -- CAMBIAR: Tipo y nombre real
    usuario_solicitante NVARCHAR(50),       -- CAMBIAR: Tipo y nombre real
    email_notificacion NVARCHAR(100),       -- CAMBIAR: Tipo y nombre real
    codigo_respuesta INTEGER,               -- CAMBIAR: Tipo y nombre real
    id_aplicacion NUMERIC,                  -- CAMBIAR: Tipo y nombre real
    codigo_respuesta_ext NVARCHAR(10),      -- CAMBIAR: Tipo y nombre real
    descripcion_respuesta NVARCHAR(500),    -- CAMBIAR: Tipo y nombre real
    fecha_respuesta DATETIME2,              -- CAMBIAR: Tipo y nombre real
    numero_reintentos INTEGER,              -- CAMBIAR: Tipo y nombre real
    estado_operacion INTEGER,               -- CAMBIAR: Tipo y nombre real
    
    -- Campos de auditoria
    fecha_creacion DATETIME2 DEFAULT GETDATE(),
    fecha_actualizacion DATETIME2 DEFAULT GETDATE()
)
WITH (
    -- CAMBIAR: Estrategia de distribucion
    DISTRIBUTION = HASH(id_registro),
    -- CAMBIAR: Estrategia de particion
    CLUSTERED COLUMNSTORE INDEX
);

-- COMENTARIOS PARA DOCUMENTACION
-- EXEC sp_addextendedproperty 'MS_Description', 'Tabla para {table_name} - Cargada desde Oracle', 'SCHEMA', '{schema}', 'TABLE', '{table_name}';
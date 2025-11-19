-- Tabla de staging para: tpp_recarga
-- AUTOGENERADO - Campos ficticios, REEMPLAZAR con estructura real

DECLARE table_exists BOOL;

SET table_exists = (
  SELECT COUNT(1) > 0
  FROM `${PROJECT_NAME}.staging_dataset.INFORMATION_SCHEMA.TABLES`
  WHERE table_name = 'stg_tpp_recarga'
);

IF NOT table_exists THEN
  CREATE TABLE `${PROJECT_NAME}.staging_dataset.stg_tpp_recarga` (
    -- CAMBIAR: Definir la estructura real de campos aqui
    id_registro NUMERIC,                    -- CAMBIAR: Tipo y nombre real
    codigo_transaccion STRING,              -- CAMBIAR: Tipo y nombre real
    tipo_canal INTEGER,                     -- CAMBIAR: Tipo y nombre real
    sistema_origen INTEGER,                 -- CAMBIAR: Tipo y nombre real
    codigo_producto INTEGER,                -- CAMBIAR: Tipo y nombre real
    numero_cliente NUMERIC,                 -- CAMBIAR: Tipo y nombre real
    digito_verificador STRING,              -- CAMBIAR: Tipo y nombre real
    numero_operacion NUMERIC,               -- CAMBIAR: Tipo y nombre real
    monto_operacion NUMERIC,                -- CAMBIAR: Tipo y nombre real
    fecha_solicitud DATETIME,               -- CAMBIAR: Tipo y nombre real
    usuario_solicitante STRING,             -- CAMBIAR: Tipo y nombre real
    email_notificacion STRING,              -- CAMBIAR: Tipo y nombre real
    codigo_respuesta INTEGER,               -- CAMBIAR: Tipo y nombre real
    id_aplicacion NUMERIC,                  -- CAMBIAR: Tipo y nombre real
    codigo_respuesta_ext STRING,            -- CAMBIAR: Tipo y nombre real
    descripcion_respuesta STRING,           -- CAMBIAR: Tipo y nombre real
    fecha_respuesta DATETIME,               -- CAMBIAR: Tipo y nombre real
    numero_reintentos INTEGER,              -- CAMBIAR: Tipo y nombre real
    estado_operacion INTEGER,               -- CAMBIAR: Tipo y nombre real
    
    -- Campos de auditoria (opcionales)
    fecha_creacion DATETIME DEFAULT CURRENT_DATETIME(),
    fecha_actualizacion DATETIME DEFAULT CURRENT_DATETIME()
  );
END IF

-- Tabla destino para: tpp_recarga
-- AUTOGENERADO - Ajustar particion y clustering segun necesidades

DECLARE table_exists BOOL;
DECLARE primary_key_exists BOOL;

SET table_exists = (
  SELECT COUNT(1) > 0
  FROM `${PROJECT_NAME}.dep_de_apoyo_filiales_tapp.INFORMATION_SCHEMA.TABLES`
  WHERE table_name = 'dep_tpp_recarga'
);

SET primary_key_exists = (
  SELECT COUNT(1) > 0
  FROM `${PROJECT_NAME}.dep_de_apoyo_filiales_tapp.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_name = 'dep_tpp_recarga' AND column_name IN ("id_registro")
);

IF NOT table_exists THEN
  CREATE TABLE `${PROJECT_NAME}.dep_de_apoyo_filiales_tapp.dep_tpp_recarga` (
    -- CAMBIAR: Estructura de campos reales
    id_registro NUMERIC,
    codigo_transaccion STRING,
    tipo_canal INTEGER,
    sistema_origen INTEGER,
    codigo_producto INTEGER,
    numero_cliente NUMERIC,
    digito_verificador STRING,
    numero_operacion NUMERIC,
    monto_operacion NUMERIC,
    fecha_solicitud DATETIME,
    usuario_solicitante STRING,
    email_notificacion STRING,
    codigo_respuesta INTEGER,
    id_aplicacion NUMERIC,
    codigo_respuesta_ext STRING,
    descripcion_respuesta STRING,
    fecha_respuesta DATETIME,
    numero_reintentos INTEGER,
    estado_operacion INTEGER,
    fecha_creacion DATETIME DEFAULT NULL,
    fecha_actualizacion DATETIME DEFAULT NULL
  )
  -- CAMBIAR: Estrategia de particion (usar campo de fecha apropiado)
  PARTITION BY DATETIME_TRUNC(fecha_respuesta, DAY)
  -- CAMBIAR: Campos de clustering segun patrones de consulta
  CLUSTER BY tipo_canal, codigo_producto
  OPTIONS(
    labels=[
      ('origen', 'proybd'), 
      ('ambiente', 'analitico'),
      ('producto', 'migracion_tapp')
    ]
  );
END IF;

IF NOT primary_key_exists THEN
  -- CAMBIAR: Campo de llave primaria real
  ALTER TABLE `${PROJECT_NAME}.dep_de_apoyo_filiales_tapp.dep_tpp_recarga`
  ADD PRIMARY KEY (id_registro) NOT ENFORCED;
END IF

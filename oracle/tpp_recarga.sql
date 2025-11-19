-- Script de extraccion para tabla: TPP_RECARGA
-- AUTOGENERADO - NO MODIFICAR MANUALMENTE
-- Campos ficticios - REEMPLAZAR con la estructura real de tu tabla

SELECT
    ID_REGISTRO,                    -- CAMBIAR: Campo identificador unico
    CODIGO_TRANSACCION,             -- CAMBIAR: Codigo de transaccion
    TIPO_CANAL,                     -- CAMBIAR: Tipo de canal (ej: web, movil, sucursal)
    SISTEMA_ORIGEN,                 -- CAMBIAR: Sistema que origina el dato
    CODIGO_PRODUCTO,                -- CAMBIAR: Codigo del producto
    NUMERO_CLIENTE,                 -- CAMBIAR: Numero/RUT del cliente
    DIGITO_VERIFICADOR,             -- CAMBIAR: Digito verificador
    NUMERO_OPERACION,               -- CAMBIAR: Numero de operacion/contrato
    MONTO_OPERACION,                -- CAMBIAR: Monto de la operacion
    TO_CHAR(FECHA_SOLICITUD, 'YYYY-MM-DD HH24:MI:SS') AS FECHA_SOLICITUD,  -- CAMBIAR: Fecha de solicitud
    USUARIO_SOLICITANTE,            -- CAMBIAR: Usuario que realiza la solicitud
    EMAIL_NOTIFICACION,             -- CAMBIAR: Email para notificaciones
    CODIGO_RESPUESTA,               -- CAMBIAR: Codigo de respuesta del sistema
    ID_APLICACION,                  -- CAMBIAR: ID de aplicacion externa
    CODIGO_RESPUESTA_EXT,           -- CAMBIAR: Codigo respuesta externa
    DESCRIPCION_RESPUESTA,          -- CAMBIAR: Descripcion de la respuesta
    TO_CHAR(FECHA_RESPUESTA, 'YYYY-MM-DD HH24:MI:SS') AS FECHA_RESPUESTA,  -- CAMBIAR: Fecha de respuesta
    NUMERO_REINTENTOS,              -- CAMBIAR: Numero de reintentos
    ESTADO_OPERACION                -- CAMBIAR: Estado de la operacion
FROM
    TPP.TPP_RECARGA      -- CAMBIAR: Schema y nombre de tabla real

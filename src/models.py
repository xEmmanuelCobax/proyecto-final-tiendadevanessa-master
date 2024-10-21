import config


# NOTAS:


class MyException(Exception):
    def __init__(self, Tipo, mensaje):
        self.Tipo = Tipo
        self.mensaje = mensaje


def ConsultaPIA():
    Cpia = []
    Cpia = config.Read(
        """
    SELECT 
        proyecto.almacen.ID_PRODUCTO,
        proyecto.almacen.NOMBRE, 
        proyecto.almacen.PRECIO_UNITARIO, 
        proyecto.almacen.EXISTENCIAS,
        proyecto.almacen.PRECIO_EXISTENCIA, 
        proyecto.intermediario.NOMBRE,
        proyecto.intermediario.AP_PAT,
        proyecto.intermediario.AP_MAT,
        proyecto.intermediario.TEL,
        proyecto.proveedor.NOMBRE
    FROM proyecto.proveedor, proyecto.intermediario, proyecto.almacen
    WHERE proyecto.proveedor.ID_COMPANIA = proyecto.intermediario.ID_COMPANIA
    AND proyecto.intermediario.ID_INTERMEDIARIO = proyecto.almacen.ID_INTERMEDIARIO
    AND proyecto.almacen.ESTATUS = 1

    ORDER BY 
    proyecto.almacen.ID_PRODUCTO ASC;
        """
    )
    return Cpia


def ConsultaIntermediarios():
    Intermediarios = []
    Intermediarios = config.Read(
        """
        SELECT 
            proyecto.proveedor.ID_COMPANIA,
            proyecto.proveedor.NOMBRE,
            proyecto.intermediario.ID_INTERMEDIARIO,
            proyecto.intermediario.NOMBRE, 
            proyecto.intermediario.AP_PAT, 
            proyecto.intermediario.AP_MAT 
        FROM proyecto.proveedor 
        INNER JOIN proyecto.intermediario ON proyecto.intermediario.ID_COMPANIA = proyecto.proveedor.ID_COMPANIA 
        WHERE proyecto.proveedor.ESTATUS = 1 
        AND proyecto.intermediario.ESTATUS = 1;
        """
    )
    return Intermediarios


def ConsultaCompanias():
    companias = []
    companias = config.Read(
        """
        SELECT 
            proyecto.proveedor.ID_COMPANIA, 
            proyecto.proveedor.NOMBRE  
        FROM proyecto.proveedor  
        WHERE proyecto.proveedor.ESTATUS = 1 ;
        """
    )
    return companias
# endregion

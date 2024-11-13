from db import Read, CUD


# NOTAS:
# Usar la importacion para evitar conflictos:

# region PIA
def ConsultaPIA():
    Cpia = []
    Cpia = Read("CALL ConsultaPIA();"
    )
    return Cpia
# endregion

# region Int
def ConsultaIntermediarios():
    Intermediarios = []
    Intermediarios = Read(
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
# endregion

# region comp
def ConsultaCompanias():
    companias = []
    companias = Read(
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

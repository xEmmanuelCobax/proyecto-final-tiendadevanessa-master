import config
from datetime import date
from datetime import datetime

print("<#################### addsalesworker ####################")
# Supongamos que nos da una matriz de formato [id,nombre,precio,disponibilidad,]
products = [
    [1, "Coca_Cola_500ml", 18, 99, 1782,2],
    [2, "Cheetos_250gr", 15, 99, 1485,3],
    [3, "Doritos_250gr", 22, 99, 2178,4],
    [4, "Takis_Hexa_250gr", 18, 200, 3600,4],
]

# Verificar que existe en la base de datos>
ValidarExistencia = False
for i in range(len(products)):
    ExisteProducto = config.Read(
        """
        SELECT dbo.Almacen.ID_PRODUCTO 
        FROM dbo.Almacen 
        WHERE dbo.Almacen.ESTATUS = 1 
        AND dbo.Almacen.ID_PRODUCTO=?
        """,
        (products[i][0],)
    )
    if not ExisteProducto:
        ValidarExistencia = False
        break
    ValidarExistencia = True

if ValidarExistencia == True:
    print("Todos los productos existen")
    # Fecha actual
    x = datetime.now()
    day = x.strftime("%d")
    month = x.strftime("%m")
    year = x.strftime("%Y")
    print(day, month, year)

    # Inicializar new como una lista de listas vacías
    new = [[] for _ in range(len(products))]

    CostSum = 0
    IvaSum = 0

    for i in range(len(products)):
        # Operaciones
        Cost = (products[i][2]) * (products[i][5])
        IvaValue = Cost * 0.16  # Asumiendo que el IVA es del 16%
        CostSum += Cost
        IvaSum += IvaValue
        # Apartado en donde se agregar datos a array
        new[i].append(products[i][5]) # CANTIDAD
        new[i].append(Cost)  # IMPORTE
        new[i].append(IvaValue)  # IVA
        new[i].append(products[i][0]) # ID_PRODUCTO

    print("Tabla resultante")
    for aux in new:
        print(aux)

    print("Total venta:", CostSum)
    print("Total iva:", IvaSum)
    print("Total:",CostSum+IvaSum)
    


else:
    print("No existe producto")
print("#################### FIN ####################>")

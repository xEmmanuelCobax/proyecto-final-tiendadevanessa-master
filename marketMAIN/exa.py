import config, locale
from datetime import datetime
locale.setlocale(locale.LC_TIME, "es_ES")
try:
    print("<#################### addsalesworker ####################")
    # Supongamos que nos da una matriz de formato [id,Cantidad a vender]
    Entrada = [
        [1,2],
        [2,3],
        [3,4],
    ]
    # Inicializar new como una lista de listas vacías
    tabla = [[] for _ in range(len(Entrada))]
    # Verificar que existe en la base de datos>
    ValidarExistencia = False
    for i in range(len(Entrada)):
        ExisteProducto = config.Read(
            """
            SELECT 
                dbo.Almacen.ID_PRODUCTO,
				dbo.Almacen.PRECIO_UNITARIO,
				dbo.Almacen.EXISTENCIAS
            FROM dbo.Almacen 
            WHERE dbo.Almacen.ESTATUS = 1 
            AND dbo.Almacen.ID_PRODUCTO = ?
            """,
            (Entrada[i][0],),
        )
        tabla[i].append(ExisteProducto[0][0])
        tabla[i].append(ExisteProducto[0][1])
        tabla[i].append(ExisteProducto[0][2])
        # Si un producto no existe, entonces terminamos el ciclo y el booleano ValidarExistencia es falso
        if not ExisteProducto:
            ValidarExistencia = False
            break
        # Si no hay errores entonces el booleano ValidarExistencia es verdadero
        ValidarExistencia = True
    for producto in tabla:
        print(producto)
    # Si los productos existen(Estan activos) y estan en la BD entonces>
    if ValidarExistencia == True:
        # Obtenemos la fecha actual
        Auxiliar = datetime.now()
        # Datos utiles para fecha
        DiaA = Auxiliar.strftime("%d")  # Dia
        MesA = Auxiliar.strftime("%B")  # Mes
        AnioA = Auxiliar.strftime("%Y")  # Anio
        # Imprimir
        print(DiaA, MesA, AnioA)

        # Encontrar ID_DIA en BD DIA
        Dia = int(
            config.Read(
                """
            SELECT dbo.Dia.ID_DIA 
            FROM dbo.Dia 
            WHERE dbo.Dia.DIA = ?
            """,
                (DiaA),
            )[0][0]
        )
        # Encontrar ID_MES en BD MES
        Mes = int(
            config.Read(
                """SELECT dbo.Mes.ID_MES 
            FROM dbo.Mes 
            WHERE dbo.Mes.MES = ?
            """,
                (MesA),
            )[0][0]
        )
        # Encontrar ID_ANIO en BD ANIO
        Anio = int(
            config.Read(
                """
            SELECT dbo.Anio.ID_ANIO 
            FROM dbo.Anio 
            WHERE dbo.Anio.ANIO = ?
            """,
                (AnioA),
            )[0][0]
        )
        # Valores en 0
        SumaCosto = 0 # Sumatoria del costo
        SumaIva = 0 # Sumatoria del iva
        TotalProductos = 0 # Sumatoria de la cantidad de productos
        # Recorrer productos con un for
        # Inicializar new como una lista de listas vacías
        TablaDetalles = [[] for _ in range(len(Entrada))]
        ErrorVenta = False
        for i in range(len(Entrada)):
            # Datos
            """
            tabla[i][0] = ID_Producto
            tabla[i][1] = Costo Unitario
            tabla[i][2] = Stock
            Entrada[i][0] = ID_Producto
            Entrada[i][1] = Cantidad de compra
            """
            if (tabla[i][2] - Entrada[i][1]<0):
                print("Error")
                ErrorVenta = True
                break
            else:
                # Operaciones
                Cost = (tabla[i][1]) * (Entrada[i][1])  # Costo por producto
                IvaValue = Cost * 0.16  # Asumiendo que el IVA es del 16%
                SumaCosto += Cost  # Sumar los costos por producto
                SumaIva += IvaValue  # Sumar los iva por producto
                TotalProductos += Entrada[i][1]  # Sumar la cantidad de productos
                # Apartado en donde se agregar datos a array
                TablaDetalles[i].append(Entrada[i][1])  # CANTIDAD
                TablaDetalles[i].append(Cost)  # IMPORTE
                TablaDetalles[i].append(IvaValue)  # IVA
                TablaDetalles[i].append(tabla[i][0])  # ID_PRODUCTO
        if not ErrorVenta:
            # Datos
            Total = SumaCosto + SumaIva  # Costo de la venta
            print("Total venta:", SumaCosto)
            print("Total iva:", SumaIva)
            # BD
            print("Total de productos vendidos:", TotalProductos)
            print("Total con iva:", Total)
            # cuds
            config.CUD(
                """
                INSERT INTO dbo.Ventas (CANTIDAD_VENTA, TOTAL, ESTATUS, ID_DIA, ID_MES, ID_ANIO) 
                VALUES (?,?,1,?,?,?)
                """,
                (int(TotalProductos), float(Total), int(Dia), int(Mes), int(Anio)),
            )
            id=int(config.Read("SELECT IDENT_CURRENT('dbo.Ventas') AS NewID")[0][0])
            #
            print("ID-VENTA>", id)
            for y in range(len(TablaDetalles)):
                config.CUD(
                    """
                    INSERT INTO dbo.Detalles(CANTIDAD,IMPORTE,IVA,ESTATUS,ID_PRODUCTO,ID_VENTA) 
                    VALUES (?,?,?,1,?,?)
                    """,
                    (
                        int(TablaDetalles[y][0]),
                        float(TablaDetalles[y][1]),
                        float(TablaDetalles[y][2]),
                        int(TablaDetalles[y][3]),
                        int(id),
                    ),
                )
    else:
        print("No existe producto")
    print("#################### FIN ####################>")
except Exception as e:
    print(e)

#
import locale
import json
# import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
# importar modelos para query
from models.queries import (
    Read,
    CUD,
    ConsultaPIA,
    ConsultaCompanias,
    ConsultaIntermediarios,
)
# importar las excepciones
from models.exceptions import MyException
# importar las extenciones
from extensions import login_manager
#
from datetime import datetime
#
from flask_login import login_user, logout_user, login_required, current_user
#
import locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

# NOTAS:


# locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

sales = Blueprint("sales", __name__, url_prefix="/sales")


# region Agregar Ventas
@sales.route("/addsalesworker", methods=["GET", "POST"])
@login_required
def addsalesworker():
    # Errores
    ErrorCantidad = False
    ErrorPrecio = False
    ErrorProductoInexistente = False
    # Capa 1: Verificar si el usuario está autenticado
    if current_user.is_authenticated:

        if request.method == "POST":
            try:
                print("<#################### MakeSales ####################")
                sales_data = request.get_json()
                Entrada = []
                print("Sales Data Received:", sales_data)
                for i in range(len(sales_data)):
                    id = sales_data[i].get("id")
                    cantidad = sales_data[i].get("quantity")
                    print("ID>", id)  # El id
                    print("cantidad>", cantidad)
                    Entrada.append([int(id), int(cantidad)])
                #
                print("<==================== DATOS OBTENIDOS ====================")
                for producto in Entrada:
                    print(producto)
                print("========================================>")
                # Inicializar new como una lista de listas vacías
                tabla = [[] for _ in range(len(Entrada))]
                # Verificar que existe en la base de datos>
                print("Paso 1: verificar existencia del producto")
                ValidarExistencia = False
                for i in range(len(Entrada)):
                    ExisteProducto = Read(
                        "CALL GetProductoExistente(%s);",
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
                if ValidarExistencia == False:

                    raise MyException(
                        "ErrorEntrada",
                        "Se intentaron cambiar los datos.",
                    )
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
                    print("Paso 1: Encontrar ID_DIA en BD DIA")
                    Dia = int(
                        Read(
                        "CALL GetDiaId(%s);",
                        (DiaA,)
                        )[0][0]
                    )

                    # Encontrar ID_MES en BD MES
                    print("Paso 2: Encontrar ID_MES en BD MES")
                    Mes = int(
                        Read(
                        "CALL GetIdMesByNombre(%s);", 
                            (MesA,)
                        )
                        [0][0]
                    )
                    # Encontrar ID_ANIO en BD ANIO
                    print("Paso 3: Encontrar ID_ANIO en BD ANIO")
                    Anio = int(
                        Read(
                            "CALL GetIdAnioByNombre(%s);",  # Llamada al procedimiento almacenado
                        (AnioA,)  # Aquí pasa el valor de 'AnioA' como parámetro
                        )[0][0]
                    )
                    # Valores en 0
                    SumaCosto = 0  # Sumatoria del costo
                    SumaIva = 0  # Sumatoria del iva
                    TotalProductos = 0  # Sumatoria de la cantidad de productos
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
                        if tabla[i][2] - Entrada[i][1] < 0:
                            print("Error en la venta")
                            ErrorVenta = True
                            break
                        else:
                            # Operaciones
                            # Costo por producto
                            Cost = (tabla[i][1]) * (Entrada[i][1])
                            IvaValue = Cost * 0.16  # Asumiendo que el IVA es del 16%
                            SumaCosto += Cost  # Sumar los costos por producto
                            # Sumar los iva por producto
                            SumaIva += round(IvaValue)
                            TotalProductos += Entrada[i][
                                1
                            ]  # Sumar la cantidad de productos
                            # Apartado en donde se agregar datos a array
                            TablaDetalles[i].append(Entrada[i][1])  # CANTIDAD
                            TablaDetalles[i].append(Cost)  # IMPORTE
                            TablaDetalles[i].append(round(IvaValue))  # IVA
                            TablaDetalles[i].append(tabla[i][0])  # ID_PRODUCTO
                    if ErrorVenta:

                        raise MyException(
                            "ErrorVenta",
                            "No hay existencias para reaelizar la venta.",
                        )

                    if not ErrorVenta:
                        # Datos
                        Total = SumaCosto + SumaIva  # Costo de la venta
                        print("Total venta:", SumaCosto)
                        print("Total iva:", SumaIva)
                        # BD
                        print("Total de productos vendidos:", TotalProductos)
                        print("Total con iva:", Total)
                        #
                        id = CUD(
                            """
                            INSERT INTO proyecto.ventas (CANTIDAD_VENTA, TOTAL, ESTATUS, ID_DIA, ID_MES, ID_ANIO)
                            VALUES (?,?,1,?,?,?)
                            """,
                            (
                                int(TotalProductos),
                                float(Total),
                                int(Dia),
                                int(Mes),
                                int(Anio),
                            ),
                        )
                        #
                        print("ID-VENTA>", id)
                        for y in range(len(TablaDetalles)):
                            CUD(
                                """
                                INSERT INTO proyecto.detalles(CANTIDAD,IMPORTE,IVA,ESTATUS,ID_PRODUCTO,ID_VENTA)
                                VALUES (?,?,?,1,?,?);
                                """,
                                (
                                    int(TablaDetalles[y][0]),
                                    float(TablaDetalles[y][1]),
                                    float(TablaDetalles[y][2]),
                                    int(TablaDetalles[y][3]),
                                    int(id),
                                ),
                            )
                        for z in range(len(TablaDetalles)):
                            RestarProductos = int(tabla[z][2] - Entrada[z][1])
                            if RestarProductos == 0:
                                ESTATUS = 0
                            else:
                                ESTATUS = 1
                            CUD(
                                """
                                UPDATE proyecto.almacen
                                SET
                                    EXISTENCIAS = ?,
                                    PRECIO_EXISTENCIA = ?,
                                    ESTATUS = ?
                                WHERE ID_PRODUCTO = ?
                                """,
                                (
                                    int(tabla[z][2] - Entrada[z][1]),
                                    int(tabla[i][1] *
                                        (tabla[z][2] - Entrada[z][1])),
                                    ESTATUS,
                                    int(tabla[z][0]),
                                ),
                            )

                        return jsonify({"message": "Venta procesada con éxito"}), 200
            except Exception as e:
                print(e)
                flash('Ha ocurrido un error, intentelo de nuevo.', 'danger')
                return jsonify({"message": "Error en la venta. Intente nuevamente."}), 500

        # Siempre se envia estos datos
        products = Read(
         "CALL GetProductosActivos();"
        )
        print(
            "#################### FIN (sales/add-sales-worker.html) ####################>"
        )

        return render_template(
            "sales/add-sales-worker.html",
            products=products,
            ErrorCantidad=ErrorCantidad,
            ErrorPrecio=ErrorPrecio,
            ErrorProductoInexistente=ErrorProductoInexistente,
            tipo=current_user.get_tipo_usuario(),
        )
    print("#################### NO HAY SESIÓN ####################>")
    return redirect(url_for("main.index"))
# endregion




@sales.route("/reportsales", methods=["POST", "GET"])
@login_required
def reportsales():
    print("<#################### reportsales ####################")
    # Capa 1: Verificar si el usuario está autenticado
    if current_user.is_authenticated:
        tipo_usuario = current_user.get_tipo_usuario()
        # Capa 2: Verificar si el usuario es administrador
        if tipo_usuario not in ["Admin", "Gerente"]:
            flash("Esta seccion es solo para gerentes o administradores", "danger")
            # Redirige a la URL anterior o a una página por defecto
            return redirect(request.referrer or url_for("products.warehouse"))

        # Capa 3: Procesar la solicitud POST
        if request.method == "POST":
            sale_id = request.form.get("sale_id")
            print("este es el id para detalles de venta: "+ sale_id)
            
            details = Read(
                "CALL GetDetallesVenta(%s);", (sale_id,), )
           
            sales = Read( "CALL GetSales();" )
            return render_template(
                "sales/report-sales.html",
                sales=sales,
                details=details,
            )

        # Capa 4: Obtener todas las ventas si no hay método POST
        print("<==================== DATOS OBTENIDOS ====================")
        sales = Read( "CALL GetSales();" )

        # Consulta de ventas mensuales si no se envía solicitud POST
        ventas_mensuales = Read( "CALL GetVentasMensuales();")

        # Consulta del promedio de ventas mensuales
        promedio_ventas_mensuales = Read(
            """
            SELECT
                ID_MES,
                ROUND(AVG(total), 2) AS promedio_ventas_mensual
            FROM
                proyecto.ventas
            GROUP BY
                ID_MES
            ORDER BY
                ID_MES;
            """
        )

        # Consulta de ventas diarias para el día actual
        ventas_diarias = Read(
            """
            SELECT 
                COUNT(v.ID_VENTA) AS NUMERO_DE_VENTAS
            FROM 
                ventas v
            JOIN 
                dia d ON v.ID_DIA = d.ID_DIA
            JOIN 
                mes m ON v.ID_MES = m.ID_MES
            JOIN 
                anio a ON v.ID_ANIO = a.ID_ANIO
            WHERE 
                CONCAT(a.anio, '-', LPAD(m.ID_MES, 2, '0'), '-', LPAD(d.dia, 2, '0')) = CURDATE()
            GROUP BY 
                DIA;
            """
        )
        print("consulta de ventas_diarias")
        print(ventas_diarias)
        print("aqui termina")

        # Si no hay ventas en el día actual, lo establecemos como cero

        if ventas_diarias:
            ventas_diarias_totales = ventas_diarias[0][0]  # El primer valor de la primera fila es el total de ventas
        else:
            ventas_diarias_totales = 0


        # Convertimos los resultados en un formato adecuado para JSON
        # ventas_mensuales = [item["NUMERO_DE_VENTAS"]
        #                     for item in ventas_mensuales]
        
        print(ventas_diarias_totales)  # Verifica que tienes todos los meses
        print(ventas_mensuales)  # Verifica que tienes todos los meses

        print(promedio_ventas_mensuales)  # Verifica que tienes todos los meses

        print(f"products > {sales}")
        print(f"products > {sales}")
        print("========================================>")
        print(
            "#################### FIN RenderT(products/warehouse.html) ####################>"
        )
        return render_template(
            "sales/report-sales.html", sales=sales, ventas_mensuales=ventas_mensuales, promedio_ventas=promedio_ventas_mensuales,  ventas_diarias_totales=ventas_diarias_totales

        )
    print("#################### NO HAY SESIÓN ####################>")
    return redirect(url_for("main.index"))

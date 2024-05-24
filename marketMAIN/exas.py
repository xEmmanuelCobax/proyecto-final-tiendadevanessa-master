import config

class MyException(Exception):
    def __init__(self, Tipo, mensaje):
        self.Tipo = Tipo
        self.mensaje = mensaje
        
try:
                # Obtener datos del formulario
                marca = ""
                producto = ""
                # Unidad de medida
                unit_quantity = 24  # Cantidad
                seslect_unit_quantity = "liters"
                # Construir la cantidad con la unidad de medida
                if seslect_unit_quantity == "pieces":
                    quantity = unit_quantity + "Pzs"
                elif seslect_unit_quantity == "liters":
                    quantity = unit_quantity + "l"
                elif seslect_unit_quantity == "milliliters":
                    quantity = unit_quantity + "ml"
                elif seslect_unit_quantity == "kilogram":
                    quantity = unit_quantity + "kg"
                elif seslect_unit_quantity == "grams":
                    quantity = unit_quantity + "gr"
                else:
                    quantity = unit_quantity + "No se"
                # Datos formados
                nombre = f"{marca}_{producto}_{quantity}"
                cantidad = 200
                precio = 20
                compania = 1
                intermediario = 1
                # Pruebas
                print("<==================== DATOS OBTENIDOS ====================")
                print(f"nombre - {nombre}")
                print(f"cantidad - {cantidad}")
                print(f"precio - {precio}")
                print(f"compania - {compania}")
                print(f"intermediario - {intermediario}")
                print("========================================>")
                # Verificar las condiciones de existencia y relación de la compañía e intermediario
                print(
                    "<==================== VERIFICAR RELACION COMPANIA - INTERMEDIARIO ===================="
                )
                existe = config.Read(
                    """
                    SELECT 
                        ID_INTERMEDIARIO, 
                        Intermediario.NOMBRE, 
                        Intermediario.AP_PAT, 
                        Intermediario.AP_MAT, 
                        Proveedor.ID_COMPANIA, 
                        Proveedor.NOMBRE 
                    FROM dbo.Proveedor 
                    INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA 
                    WHERE dbo.Proveedor.ESTATUS = 1 AND dbo.Intermediario.ESTATUS = 1 
                    AND dbo.Intermediario.ID_INTERMEDIARIO = ? 
                    AND dbo.Proveedor.ID_COMPANIA = ?
                    """,
                    (intermediario, compania),
                )
                print("========================================>")
                print("<==================== productoinactivo ====================")
                productoinactivo = config.Read(
                    """
                    SELECT 
                        dbo.Almacen.ID_PRODUCTO,
                        dbo.Almacen.NOMBRE 
                    FROM dbo.Almacen 
                    WHERE dbo.Almacen.NOMBRE = ?
                    AND dbo.Almacen.ESTATUS = 0
                    """,
                    (nombre,),
                )
                print("========================================>")
                # Verificar si el producto ya existe
                print("<==================== productoexiste ====================")
                productoexiste = config.Read(
                    """
                    SELECT 
                        dbo.Almacen.NOMBRE 
                    FROM dbo.Almacen 
                    WHERE dbo.Almacen.NOMBRE = ?
                    AND dbo.Almacen.ESTATUS = 1
                    """,
                    (nombre,),
                )
                print("========================================>")
                # Condiciones
                print("<==================== ACCIONES ====================")
                if productoexiste:
                    # Si el producto ya existe, redireccionar con un mensaje de error
                    print(
                        "====================! Existing product in the DB.====================>"
                    )
                    raise MyException(
                        "OtherError",
                        "The company or the intermediary does not meet the necessary conditions.",
                    )
                elif productoinactivo:
                    print(
                        "====================! Producto existente (Oculto) en la BD.====================>"
                    )
                    product_id = productoinactivo[0][0]

                    config.CUD(
                        """
                        UPDATE dbo.Almacen 
                        SET 
                            PRECIO_UNITARIO = ?, 
                            EXISTENCIAS = ?, 
                            PRECIO_EXISTENCIA = ?, 
                            ID_INTERMEDIARIO = ?, 
                            ESTATUS = 1 
                        WHERE ID_PRODUCTO = ?
                        """,
                        (
                            precio,
                            cantidad,
                            float(precio) * int(cantidad),
                            intermediario,
                            product_id,
                        ),
                    )
                elif existe:
                    # Insertar el nuevo producto en la base de datos
                    config.CUD(
                        """
                        INSERT INTO dbo.Almacen (NOMBRE, PRECIO_UNITARIO, EXISTENCIAS, PRECIO_EXISTENCIA, ID_INTERMEDIARIO, ESTATUS)
                        VALUES (?, ?, ?, ?, ?, 1)
                        """,
                        (
                            nombre,
                            precio,
                            cantidad,
                            float(precio) * int(cantidad),
                            intermediario,
                        ),
                    )
                    print(
                        "====================!Producto creado exitosamente.!====================>"
                    )
                    print("#################### FIN ####################>")
                else:
                    # Si la compañía o el intermediario no cumplen las condiciones, redireccionar con un mensaje de error
                    print(
                        "====================!La compañía o el intermediario no cumplen las condiciones necesarias.====================>"
                    )
                    raise MyException(
                        "OtherError",
                        "The company or the intermediary does not meet the necessary conditions.",
                    )
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                print("#################### FIN ####################>")
            except Exception as e:
                print(f"Type: {e}")
                print("#################### FIN ####################>")
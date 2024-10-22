# import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# importar modelos para query
from models.queries import Read, CUD, ConsultaPIA, ConsultaCompanias, ConsultaIntermediarios
# importar las excepciones 
from models.exceptions import MyException
# importar las extenciones
from extensions import login_manager


# NOTAS:


products = Blueprint("products", __name__, url_prefix="/products")


# region Mostrar productos
@products.route("/warehouse", methods=["GET", "POST"])
def warehouse():
    print("<#################### warehouse ####################")
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    # Capa 2: Verificar si el usuario es administrador
    if not session.get("ES_ADMIN"):
        print("#################### NO ES ADMIN ####################>")
        return redirect(url_for("shortcut.shortcut"))
    if request.method == "POST":
        search_term = (str(request.form.get("search_term"))).strip()
        # Pruebas
        print("<==================== DATOS OBTENIDOS ====================")
        print(f"nombre - {search_term}")
        print("========================================>")
        # Consulta
        products = Read(
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
            WHERE proyecto.almacen.NOMBRE LIKE ? 
            AND proyecto.proveedor.ID_COMPANIA = proyecto.intermediario.ID_COMPANIA
            AND proyecto.intermediario.ID_INTERMEDIARIO = proyecto.almacen.ID_INTERMEDIARIO
            AND proyecto.almacen.ESTATUS = 1;
            """,
            ("%" + search_term + "%",),
        )
        print(
            "#################### FIN RenderT(products/warehouse.html) ####################>"
        )
        return render_template(
            "products/warehouse.html", products=products, IsAdmin=session["ES_ADMIN"]
        )
    # Capa 3: Renderizar con los datos
    print("<==================== DATOS OBTENIDOS ====================")
    products = ConsultaPIA()
    print(f"products > {products}")
    print("========================================>")
    print(
        "#################### FIN RenderT(products/warehouse.html) ####################>"
    )
    return render_template(
        "products/warehouse.html",
        products=products,
        IsAdmin=session["ES_ADMIN"],
    )
# endregion


# region manejar productos
@products.route("/manage_products", methods=["GET", "POST"])
def manage_products():
    # Verificar autenticación y permisos
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        return redirect(url_for("index"))
    # Capa 2: Verificar si el usuario es administrador
    if not session.get("ES_ADMIN"):
        return redirect(url_for("shortcut.shortcut"))
    # Capa 3: Procesar los formularios POST
    if request.method == "POST":
        form_type = request.form.get("form_type")
        # region Borrar producto
        if form_type == "delete":
            product_id = int(request.form.get("product_id"))
            CUD(
                "UPDATE proyecto.almacen  SET ESTATUS = 0 WHERE ID_PRODUCTO = ?",
                (product_id,),
            )
            flash("El producto ha sido eliminado exitosamente.")
        # endregion
        # region Crear producto
        elif form_type == "create":
            try:
                # Obtener datos del formulario
                marca = request.form.get("marca")
                producto = request.form.get("producto")
                unit_quantity = request.form.get("unitquantity")  # Cantidad
                select_unit_quantity = request.form.get(
                    "SelectUnitOfMeasure"
                )  # Unidad de medida
                # Construir la cantidad con la unidad de medida
                if select_unit_quantity == "pieces":
                    quantity = unit_quantity + "Pzs"
                elif select_unit_quantity == "liters":
                    quantity = unit_quantity + "l"
                elif select_unit_quantity == "milliliters":
                    quantity = unit_quantity + "ml"
                elif select_unit_quantity == "kilogram":
                    quantity = unit_quantity + "kg"
                elif select_unit_quantity == "grams":
                    quantity = unit_quantity + "gr"
                else:
                    quantity = unit_quantity + "custom"
                # Errores relacionados a nombre
                if len(marca) > 35 or len(producto) > 35:
                    auxiliar = "Los siguientes campos tienen más de 35 caracteres:"
                    if len(marca) > 35:
                        auxiliar += " Marca"
                    if len(producto) > 35:
                        auxiliar += ", Nombre del producto"
                    raise MyException("MaxLength", auxiliar)
                # Datos formados
                nombre = f"{marca}_{producto}_{quantity}"
                try:
                    cantidad = int(request.form.get("cantidad"))
                except ValueError:
                    raise MyException(
                        "InvalidInput", "La cantidad debe ser un número entero válido."
                    )
                try:
                    precio = float(request.form.get("precio"))
                except ValueError:
                    raise MyException(
                        "InvalidInput", "El precio debe ser un número válido."
                    )
                try:
                    compania = int(request.form.get("company_id"))
                except ValueError:
                    raise MyException(
                        "InvalidInput",
                        "El ID de la compañía debe ser un número entero válido.",
                    )
                try:
                    intermediario = int(request.form.get("intermedary_id"))
                except ValueError:
                    raise MyException(
                        "InvalidInput",
                        "El ID del intermediario debe ser un número entero válido.",
                    )
                # Errores
                if cantidad <= 0 or precio <= 0:
                    raise MyException(
                        "NonPositive",
                        f"Los valores proporcionados {cantidad, precio} no son positivos. Deben ser mayores que cero.",
                    )
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
                existe = Read(
                    """
                    SELECT 
                        proyecto.intermediario.ID_INTERMEDIARIO, 
                        proyecto.intermediario.NOMBRE, 
                        proyecto.intermediario.AP_PAT, 
                        proyecto.intermediario.AP_MAT, 
                        proyecto.proveedor.ID_COMPANIA, 
                        proyecto.proveedor.NOMBRE 
                    FROM proyecto.proveedor 
                    INNER JOIN proyecto.intermediario ON proyecto.intermediario.ID_COMPANIA = proyecto.proveedor.ID_COMPANIA 
                    WHERE proyecto.proveedor.ESTATUS = 1 AND proyecto.intermediario.ESTATUS = 1 
                    AND proyecto.intermediario.ID_INTERMEDIARIO = ? 
                    AND proyecto.proveedor.ID_COMPANIA = ?
                    """,
                    (intermediario, compania),
                )
                print("========================================>")
                print("<==================== productoinactivo ====================")
                productoinactivo = Read(
                    """
                    SELECT 
                        proyecto.almacen.ID_PRODUCTO,
                        proyecto.almacen.NOMBRE 
                    FROM proyecto.almacen 
                    WHERE proyecto.almacen.NOMBRE = ?
                    AND proyecto.almacen.ESTATUS = 0
                    """,
                    (nombre,),
                )
                print("========================================>")
                # Verificar si el producto ya existe
                print("<==================== productoexiste ====================")
                productoexiste = Read(
                    """
                    SELECT 
                        proyecto.almacen.NOMBRE 
                    FROM proyecto.almacen 
                    WHERE proyecto.almacen.NOMBRE = ?
                    AND proyecto.almacen.ESTATUS = 1
                    """,
                    (nombre,),
                )
                print("========================================>")
                # Condiciones
                print("<==================== ACCIONES ====================")
                if productoexiste:
                    print(
                        "====================! Existing product in the DB.====================>"
                    )
                    raise MyException("ProductExists", "El producto existe")
                elif productoinactivo:
                    print(
                        "====================! Producto existente (Oculto) en la BD.====================>"
                    )
                    product_id = productoinactivo[0][0]
                    CUD(
                        """
                        UPDATE proyecto.almacen  
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
                            precio * cantidad,
                            intermediario,
                            product_id,
                        ),
                    )
                    flash("Producto creado exitosamente.")
                elif existe:
                    CUD(
                        """
                        INSERT INTO proyecto.almacen (NOMBRE, PRECIO_UNITARIO, EXISTENCIAS, PRECIO_EXISTENCIA, ID_INTERMEDIARIO, ESTATUS)
                        VALUES (?, ?, ?, ?, ?, 1)
                        """,
                        (
                            nombre,
                            precio,
                            cantidad,
                            precio * cantidad,
                            intermediario,
                        ),
                    )
                    print(
                        "====================!Producto creado exitosamente.!====================>"
                    )
                    flash("Producto creado exitosamente.")
                    print("#################### FIN ####################>")
                else:
                    print(
                        "====================!La compañía o el intermediario no cumplen las condiciones necesarias.====================>"
                    )
                    raise MyException(
                        "CIConditions",
                        "La empresa o el intermediario no cumple con las condiciones necesarias.",
                    )
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN ####################>")
            except ValueError as e:
                print("La cadena no representa un número válido")
                flash("La cadena no representa un número válido")
                print("#################### FIN ####################>")
            except Exception as err:
                print(f"Inesperado {err=}, {type(err)=}")
                flash("Ocurrió un error inesperado")
                print("#################### FIN ####################>")
        # endregion
        # region Actualizar producto
        elif form_type == "update":
            try:
                # Obtener datos del formulario
                product_id = request.form.get("editproductid")
                marca = request.form.get("newmarca")
                producto = request.form.get("newproducto")
                # Unidad de medida
                unit_quantity = int(request.form.get("editunitquantity"))  # Cantidad
                seslect_unit_quantity = request.form.get(
                    "EditSelectUnitOfMeasure"
                )  # Unidad de medida
                # Piezas
                if seslect_unit_quantity == "pieces":
                    quantity = str(unit_quantity) + "Pzs"
                # Litros
                elif seslect_unit_quantity == "liters":
                    quantity = str(unit_quantity) + "l"
                # Milimetros
                elif seslect_unit_quantity == "milliliters":
                    quantity = str(unit_quantity) + "ml"
                # Kilogramos
                elif seslect_unit_quantity == "kilogram":
                    quantity = str(unit_quantity) + "kg"
                # Gramos
                elif seslect_unit_quantity == "grams":
                    quantity = str(unit_quantity) + "gr"
                # custom?
                else:
                    quantity = str(unit_quantity) + "custom"
                # Errores relacionados a nombre
                if len(marca) > 35 or len(producto) > 35:
                    auxiliar = "Los siguientes campos tienen más de 35 caracteres:"
                    if len(marca) > 35:
                        auxiliar += "Marca "
                    if len(producto) > 35:
                        auxiliar += ", Nombre del producto"
                    raise MyException(
                        "MaxLength",
                        auxiliar,
                    )
                # Datos formados
                nombre = f"{marca}_{producto}_{quantity}"
                cantidad = int(request.form.get("newcantidad"))
                precio = float(request.form.get("newprecio"))
                compania = int(request.form.get("company-new-select"))
                intermediario = int(request.form.get("intermedary-new-select"))
                # Errores
                if cantidad <= 0 or precio <= 0:
                    if cantidad <= 0 or precio <= 0:
                        raise MyException(
                            "NonPositive",
                            f"Los valores proporcionados {cantidad,precio} no son positivos. Deben ser mayores que cero.",
                        )
                    elif cantidad <= 0:
                        raise MyException(
                            "NonPositive",
                            f"El valor proporcionado {cantidad} no es positivo. Debe ser mayor que cero.",
                        )
                    elif precio <= 0:
                        raise MyException(
                            "NonPositive",
                            f"El valor proporcionado {precio} no es positivo. Debe ser mayor que cero.",
                        )
                # Pruebas
                print("<==================== DATOS OBTENIDOS ====================")
                print(f"product_id - {product_id}")
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
                existe = Read(
                    """
                        SELECT 
                            proyecto.intermediario.ID_INTERMEDIARIO,
                            proyecto.intermediario.NOMBRE,   
                            proyecto.intermediario.AP_PAT, 
                            proyecto.intermediario.AP_MAT, 
                            proyecto.proveedor.ID_COMPANIA, 
                            proyecto.proveedor.NOMBRE
                        FROM proyecto.proveedor
                        INNER JOIN proyecto.intermediario ON proyecto.intermediario.ID_COMPANIA = proyecto.proveedor.ID_COMPANIA 
                        WHERE proyecto.proveedor.ESTATUS = 1 
                        AND proyecto.intermediario.ESTATUS = 1 
                        AND proyecto.intermediario.ID_INTERMEDIARIO = ?
                        AND proyecto.proveedor.ID_COMPANIA = ?
                    """,
                    (
                        int(intermediario),
                        int(compania),
                    ),
                )
                print("========================================>")
                # Verificar si el producto ya existe
                print(
                    "<==================== VERIFICAR SI EL PRODUCTO EXISTE ===================="
                )
                productoexiste = Read(
                    """
                        SELECT 
                            proyecto.almacen.NOMBRE 
                        FROM proyecto.almacen 
                        WHERE proyecto.almacen.NOMBRE = ?
                        AND proyecto.almacen.ID_PRODUCTO != ?
                        AND proyecto.almacen.ESTATUS = 1
                        """,
                    (nombre, int(product_id)),
                )
                print("========================================>")
                # Condiciones
                print("<==================== ACCIONES ====================")
                if productoexiste:
                    # Si el producto ya existe con un nombre diferente, redireccionar con un mensaje de error
                    print(
                        "====================! Producto existente en la BD.====================>"
                    )
                    raise MyException(
                        "ProductExists",
                        "El producto existe",
                    )
                elif not existe:
                    # Si la compañía o el intermediario no cumplen las condiciones, redireccionar con un mensaje de error
                    print(
                        "====================! La compañía o el intermediario no cumplen las condiciones necesarias.====================>"
                    )
                    raise MyException(
                        "CIConditions",
                        "La empresa o el intermediario no cumple con las condiciones necesarias.",
                    )
                else:
                    # Actualizar el producto en la base de datos
                    CUD(
                        """
                            UPDATE proyecto.almacen 
                            SET 
                                NOMBRE = ?, 
                                PRECIO_UNITARIO = ?, 
                                EXISTENCIAS = ?, 
                                PRECIO_EXISTENCIA = ?, 
                                ID_INTERMEDIARIO = ?, 
                                ESTATUS = 1 
                            WHERE ID_PRODUCTO = ?
                            """,
                        (
                            nombre,
                            float(precio),
                            int(cantidad),
                            float(precio) * int(cantidad),
                            int(intermediario),
                            int(product_id),
                        ),
                    )
                    print(
                        "====================! Producto actualizado exitosamente. !====================>"
                    )
                    flash("Producto actualizado exitosamente.")
            except ValueError:
                print("La cadena no representa un número válido")
                flash("La cadena no representa un número válido")
                print("#################### FIN ####################>")
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN ####################>")
            except Exception as e:
                print(f"Type: {e}")
                flash(f"Type: {e}")
                print("#################### FIN ####################>")
        # endregion
    return render_template(
        "products/manage-warehouse.html",
        products=ConsultaPIA(),
        relations=ConsultaIntermediarios(),
        companies=ConsultaCompanias(),
        IsAdmin=session["ES_ADMIN"],
    )
# endregion


# region Manejar intermediario
@products.route("/manage_intermediary", methods=["GET", "POST"])
def manage_intermediary():
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    # Capa 2: Verificar si el usuario es administrador
    if not session.get("ES_ADMIN"):
        print("#################### NO ES ADMIN ####################>")
        return redirect(url_for("shortcut.shortcut"))
    #  Capa 3: Manejar la lógica del formulario POST
    if request.method == "POST":
        action = request.form.get("action")
        # region Borrar intermediario
        if action == "delete":
            try:
                print("<#################### delete ####################")
                id_intermediario = int(
                    request.form.get("DeleteIntermediaryId")
                )  # posible error en el SQL
                NoSePuedeBorrar = Read(
                    """
                    SELECT 
                        proyecto.almacen.NOMBRE
                    FROM proyecto.intermediario,proyecto.Almacen
                    WHERE proyecto.intermediario.ID_INTERMEDIARIO = proyecto.Almacen.ID_INTERMEDIARIO
                    AND proyecto.almacen.EXISTENCIAS != 0
                    AND proyecto.intermediario.ID_INTERMEDIARIO = ?
                    """,
                    (id_intermediario,),
                )
                if NoSePuedeBorrar:
                    raise MyException(
                        "Error al borrar compañia.",
                        "Para poder borrar un intermediario primero debe asegurarse que los productos relacionados sean inexistentes.",
                    )
                CUD(
                    """
                    -- Actualizar proyecto.Almacen
                    UPDATE proyecto.almacen
                    SET ESTATUS = 0
                    WHERE ID_INTERMEDIARIO = ?;
                    """,
                    (int(id_intermediario),),
                )
                CUD(
                    """
                    -- Actualizar proyecto.intermediario
                    UPDATE proyecto.intermediario
                    SET ESTATUS = 0
                    WHERE ID_INTERMEDIARIO = ?;
                    """,
                    (int(id_intermediario),),
                )
                flash("Se ha borrado correctamente el intermediario.")
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto) ####################>")
            except Exception as e:
                print(f"Type: {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto) ####################>")
        # endregion
        # region Crear intermediario
        elif action == "create":
            try:
                # Obtener datos del formulario
                nombre = request.form.get("intermediaryName")
                apellido_paterno = request.form.get("AP_PAT")
                apellido_materno = request.form.get("AP_MAT")
                telefono = int(request.form.get("intermediaryPhone"))
                company_id = int(request.form.get("company_id"))
                # Pruebas
                print("<==================== DATOS OBTENIDOS ====================")
                print(f"Nombre: {nombre}")
                print(f"Apellido Paterno: {apellido_paterno}")
                print(f"Apellido Materno: {apellido_materno}")
                print(f"Teléfono: {telefono}")
                print(f"ID de la Compañía: {company_id}")
                print("========================================>")
                # Error telefono
                if len(str(telefono)) != 10:
                    raise MyException(
                        "ErrorTel", "El número de teléfono no tiene 10 números."
                    )
                # Existe pero esta inactivo
                VerificarInactivo = Read(
                    """
                        SELECT 
                            proyecto.intermediario.ID_INTERMEDIARIO,
                            proyecto.intermediario.NOMBRE,
                            proyecto.intermediario.AP_PAT,
                            proyecto.intermediario.AP_MAT
                        FROM proyecto.intermediario 
                        WHERE proyecto.intermediario.NOMBRE = ?
                        AND proyecto.intermediario.AP_PAT = ?
                        AND proyecto.intermediario.AP_MAT = ?
                        AND proyecto.intermediario.ESTATUS = 0
                        """,
                    (nombre, apellido_paterno, apellido_materno),
                )
                # Verificar si el intermediario ya existe
                existe = Read(
                    """
                        SELECT 
                            proyecto.intermediario.NOMBRE,
                            proyecto.intermediario.AP_PAT,
                            proyecto.intermediario.AP_MAT
                        FROM proyecto.intermediario 
                        WHERE proyecto.intermediario.NOMBRE = ?
                        AND proyecto.intermediario.AP_PAT = ?
                        AND proyecto.intermediario.AP_MAT = ?
                        AND proyecto.intermediario.ESTATUS = 1
                        """,
                    (nombre, apellido_paterno, apellido_materno),
                )
                # Verificar si el teléfono ya está en uso
                tel_existe = Read(
                    """
                        SELECT 
                            proyecto.intermediario.TEL
                        FROM proyecto.intermediario 
                        WHERE proyecto.intermediario.TEL = ?
                        """,
                    (int(telefono),),
                )
                # Cualquier error
                if existe or tel_existe:
                    if existe:
                        raise MyException(
                            "ErrorIntermediary",
                            "El intermediario ya existe en el DB.",
                        )
                    if tel_existe:
                        raise MyException(
                            "ErrorTel", "El número de teléfono ya está registrado."
                        )
                if VerificarInactivo:
                    print("Caso 1: Inactivo")
                    CUD(
                        """
                            UPDATE proyecto.intermediario 
                            SET TEL=?, ID_COMPANIA=?, ESTATUS=1
                            WHERE ID_INTERMEDIARIO = ?
                            """,
                        (
                            int(telefono),
                            int(company_id),
                            VerificarInactivo[0][0],
                        ),
                    )
                else:
                    # Insertar en la base de datos si no hay errores
                    print("Caso 2: Crear")
                    CUD(
                        """
                            INSERT INTO proyecto.intermediario (NOMBRE, AP_PAT, AP_MAT, TEL, ESTATUS, ID_COMPANIA) 
                            VALUES (?, ?, ?, ?, 1, ?)
                            """,
                        (
                            nombre,
                            apellido_paterno,
                            apellido_materno,
                            int(telefono),
                            int(company_id),
                        ),
                    )
                    print(
                        "#################### FIN (Se inserto en la BD) ####################>"
                    )
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto) ####################>")
            except Exception as e:
                print(f"Type : {e}")
                flash(f"{e}")
                print("#################### FIN (No se inserto) ####################>")
        # endregion
        # region editar intermediario
        elif action == "edit":
            try:
                # Obtener datos del formulario, incluido company_id
                nombre = request.form.get("editIntermediaryName")
                apellido_paterno = request.form.get("NEW-AP_PAT")
                apellido_materno = request.form.get("NEW-AP_MAT")
                telefono = int(request.form.get("editIntermediaryPhone"))
                company_id = int(request.form.get("Edit-company_id"))
                id_intermediario = int(
                    request.form.get("EditIntermediary_id")
                )  # Se obtiene de un dato oculto
                # Pruebas
                print("<==================== DATOS OBTENIDOS ====================")
                print(f"nombre - {nombre}")
                print(f"AP_PAT - {apellido_paterno}")
                print(f"AP_MAT - {apellido_materno}")
                print(f"TEL - {telefono}")
                print(f"company_id - {company_id}")
                print(f"id_intermediario - {id_intermediario}")
                print("========================================>")
                # Error telefono
                if len(str(telefono)) != 10:
                    raise MyException(
                        "ErrorTel", "El número de teléfono no tiene 10 números."
                    )
                # Verificar si el intermediario ya existe
                existe = Read(
                    """
                    SELECT 
                        proyecto.intermediario.NOMBRE,
                        proyecto.intermediario.AP_PAT,
                        proyecto.intermediario.AP_MAT
                    FROM proyecto.intermediario 
                    WHERE proyecto.intermediario.NOMBRE = ?
                    AND proyecto.intermediario.AP_PAT = ?
                    AND proyecto.intermediario.AP_MAT = ?
                    AND proyecto.intermediario.ID_INTERMEDIARIO != ?
                    """,
                    (nombre, apellido_paterno, apellido_materno, int(id_intermediario)),
                )
                # Verificar si el teléfono ya está en uso
                tel_existe = Read(
                    """
                    SELECT 
                        proyecto.intermediario.TEL
                    FROM proyecto.intermediario 
                    WHERE proyecto.intermediario.TEL = ?
                    AND proyecto.intermediario.ID_INTERMEDIARIO != ?
                    """,
                    (telefono, int(id_intermediario)),
                )
                # Cualquier error
                if existe or tel_existe:
                    if existe:
                        raise MyException(
                            "ErrorIntermediary",
                            "El intermediario ya existe en el DB.",
                        )
                    if tel_existe:
                        raise MyException(
                            "ErrorTel", "El número de teléfono ya está registrado."
                        )
                else:
                    # Actualizar en la base de datos
                    CUD(
                        """
                        UPDATE proyecto.intermediario 
                        SET NOMBRE=?, AP_PAT=?, AP_MAT=?, TEL=?, ID_COMPANIA=?
                        WHERE ID_INTERMEDIARIO = ?
                        """,
                        (
                            nombre,
                            apellido_paterno,
                            apellido_materno,
                            int(telefono),
                            int(company_id),
                            int(id_intermediario),
                        ),
                    )
                    flash(
                        "Se ha actualizado correctamente los datos del intermediario."
                    )
                    print(
                        "Se ha actualizado correctamente los datos del intermediario."
                    )
                    print("#################### FIN ####################>")
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto) ####################>")
            except Exception as e:
                print(f"Type : {e}")
                flash(f"{e}")
                print("#################### FIN (No se inserto) ####################>")
        # endregion
    # Datos que se envian siempre
    relations = []
    relations = Read(
        """
        SELECT 
            proyecto.proveedor.ID_COMPANIA,
            proyecto.proveedor.NOMBRE,
            proyecto.intermediario.ID_INTERMEDIARIO,
            proyecto.intermediario.NOMBRE, 
            proyecto.intermediario.AP_PAT,
            proyecto.intermediario.AP_MAT, 
            proyecto.intermediario.TEL 
        FROM proyecto.proveedor 
        INNER JOIN proyecto.intermediario ON proyecto.intermediario.ID_COMPANIA = proyecto.proveedor.ID_COMPANIA 
        WHERE proyecto.proveedor.ESTATUS = 1 
        AND proyecto.intermediario.ESTATUS = 1
        """
    )
    print(
        "#################### products/manage-intermediary.html ####################>"
    )
    return render_template(
        "products/manage-intermediary.html",
        relations=relations,
        companies=ConsultaCompanias(),
        IsAdmin=session["ES_ADMIN"],
    )
# endregion


# region Manejar compañia
@products.route("/manage_company", methods=["GET", "POST"])
def manage_company():
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    # Capa 2: Verificar si el usuario es administrador
    if not session.get("ES_ADMIN"):
        print("#################### NO ES ADMIN ####################>")
        return redirect(url_for("shortcut.shortcut"))
    # Capa 3: Manejar la lógica del formulario POST
    if request.method == "POST":
        action = request.form.get("action")
        # region Borrar compañia
        if action == "delete":
            try:
                print("<#################### delete ####################")
                id_intermediario = int(
                    request.form.get("DeleteIntermediaryId")
                )  # cambiar la direccion
                NoSePuedeBorrar = Read(
                    """
                    SELECT 
                        proyecto.almacen.NOMBRE
                    FROM proyecto.proveedor,proyecto.intermediario,proyecto.almacen
                    WHERE proyecto.proveedor.ID_COMPANIA = proyecto.intermediario.ID_COMPANIA
                    AND proyecto.intermediario.ID_INTERMEDIARIO = proyecto.almacen.ID_INTERMEDIARIO
                    AND proyecto.almacen.EXISTENCIAS != 0
                    AND proyecto.proveedor.ID_COMPANIA = ?
                    """,
                    (id_intermediario,),
                )
                if NoSePuedeBorrar:
                    raise MyException(
                        "Error al borrar compañia.",
                        "Para poder borrar una compañia primero debe asegurarse que los productos relacionados sean inexistentes.",
                    )
                CUD(
                    """
                    -- Actualizar proyecto.Almacen
                    UPDATE proyecto.almacen
                    SET ESTATUS = 0
                    WHERE ID_INTERMEDIARIO IN (
                        SELECT proyecto.intermediario.ID_INTERMEDIARIO
                        FROM proyecto.proveedor
                        JOIN proyecto.intermediario ON proyecto.proveedor.ID_COMPANIA = proyecto.intermediario.ID_COMPANIA
                        WHERE proyecto.almacen.EXISTENCIAS = 0
                        AND proyecto.proveedor.ID_COMPANIA = ?
                    );
                    """,
                    (int(id_intermediario),),
                )
                CUD(
                    """
                    -- Actualizar proyecto.Intermediario
                    UPDATE proyecto.intermediario
                    SET ESTATUS = 0
                    WHERE ID_COMPANIA IN (
                        SELECT proyecto.proveedor.ID_COMPANIA
                        FROM proyecto.proveedor
                        WHERE proyecto.proveedor.ID_COMPANIA = ?
                    );
                    """,
                    (int(id_intermediario),),
                )
                CUD(
                    """
                    -- Actualizar proyecto.Proveedor
                    UPDATE proyecto.proveedor SET ESTATUS = 0 WHERE ID_COMPANIA = ?;
                    """,
                    (int(id_intermediario),),
                )
                flash("Se ha borrado correctamente la compañia.")
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto) ####################>")
            except Exception as e:
                print(f"{e}")
                flash(f"{e}")
                print("#################### FIN (No se inserto) ####################>")
        # endregion
        # region Crear compañia
        elif action == "create":
            try:
                # Obtener datos del formulario
                nombre = request.form.get("companyName")
                # Pruebas
                print("<==================== DATOS OBTENIDOS ====================")
                print(f"Nombre: {nombre}")
                print("========================================>")
                print("<==================== VerificarInactivo ====================")
                # Existe pero esta inactivo
                VerificarInactivo = Read(
                    """
                        SELECT 
                            proyecto.proveedor.ID_COMPANIA,
                            proyecto.proveedor.NOMBRE 
                        FROM proyecto.proveedor 
                        WHERE proyecto.proveedor.NOMBRE = ?
                        AND proyecto.proveedor.ESTATUS = 0
                        """,
                    (nombre,),
                )
                print("<==================== existe ====================")
                # Verificar si la compañia ya existe
                existe = Read(
                    """
                        SELECT 
                            proyecto.proveedor.NOMBRE
                        FROM proyecto.proveedor 
                        WHERE proyecto.proveedor.NOMBRE = ?
                        AND proyecto.proveedor.ESTATUS = 1
                        """,
                    (nombre,),
                )
                # Cualquier error
                if existe:
                    if existe:
                        raise MyException(
                            "Errorcompany",
                            "La empresa ya existe en la base de datos.",
                        )
                if VerificarInactivo:
                    print("<==================== Inactivo ====================")
                    CUD(
                        """
                            UPDATE proyecto.proveedor
                            SET ESTATUS=1
                            WHERE ID_COMPANIA = ?
                            """,
                        (VerificarInactivo[0][0],),
                    )
                    print(
                        "#################### FIN (Se actualizo en la BD) ####################>"
                    )
                else:
                    print("<==================== Crear ====================")
                    print(nombre)
                    # Insertar en la base de datos si no hay errores
                    CUD(
                        """
                            INSERT INTO proyecto.proveedor (NOMBRE,  ESTATUS) 
                            VALUES (?, 1)
                        """,
                        (nombre,),
                    )
                    print(
                        "#################### FIN (Se inserto en la BD) ####################>"
                    )
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto) ####################>")
            except Exception as e:
                print(f"Type : {e}")
                flash(f"Type : {e}")
                print("#################### FIN (No se inserto) ####################>")
        # endregion
        # region Editar compañia
        elif action == "edit":
            try:
                # Obtener datos del formulario, incluido company_id
                nombre = request.form.get("editcompanyName")
                id_intermediario = int(request.form.get("EditIntermediary_id"))
                # Pruebas
                print("<==================== DATOS OBTENIDOS ====================")
                print(f"nombre - {nombre}")
                print(f"id-company - {id_intermediario}")
                print("========================================>")
                # Verificar si es inactivo
                ExisteInactivo = Read(
                    """
                    SELECT 
                        proyecto.proveedor.NOMBRE,
                        proyecto.proveedor.ID_COMPANIA
                    FROM proyecto.proveedor 
                    WHERE proyecto.proveedor.NOMBRE = ?
                    AND proyecto.proveedor.ESTATUS = 0
                    """,
                    (nombre, int(id_intermediario)),
                )
                # Verificar si la campañia ya existe
                existe = Read(
                    """
                    SELECT 
                        proyecto.proveedor.NOMBRE,
                        proyecto.proveedor.ID_COMPANIA
                    FROM proyecto.proveedor 
                    WHERE proyecto.proveedor.NOMBRE = ?
                    AND proyecto.proveedor.ID_COMPANIA != ?
                    """,
                    (nombre, int(id_intermediario)),
                )
                # Cualquier error
                if existe:
                    raise MyException(
                        "ErrorCompany",
                        "La empresa ya existe en la base de datos.",
                    )
                else:
                    # Actualizar en la base de datos
                    CUD(
                        """
                        UPDATE proyecto.proveedor  
                        SET NOMBRE=?
                        WHERE  ID_COMPANIA= ?
                        """,
                        (
                            nombre,
                            int(id_intermediario),
                        ),
                    )
                    print("#################### FIN ####################>")
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto) ####################>")
            except Exception as e:
                print(f"Type : {e}")
                flash(f"Type : {e}")
                print("#################### FIN (No se inserto) ####################>")
            # endregion
    # region Datos
    relations = []
    relations = Read(
        """
        SELECT 
            proyecto.proveedor.ID_COMPANIA,
            proyecto.proveedor.NOMBRE
        FROM proyecto.proveedor 
        WHERE proyecto.proveedor.ESTATUS = 1 
        """
    )
    # endregion
    return render_template(
        "products/manage-company.html",
        relations=relations,
        companies=ConsultaCompanias(),
        IsAdmin=session["ES_ADMIN"],
    )
# endregion

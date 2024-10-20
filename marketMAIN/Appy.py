from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    session,
    jsonify,
)
# Importar config.py en donde se hacen las consultas de la base de datos
import config, locale, re 

from datetime import datetime

locale.setlocale(locale.LC_TIME, "es_ES")

class MyException(Exception):
    def __init__(self, Tipo, mensaje):
        self.Tipo = Tipo
        self.mensaje = mensaje


app = Flask(__name__)


auth = Blueprint("auth", __name__, url_prefix="/auth")
products = Blueprint("products", __name__, url_prefix="/products")
p = Blueprint("profile", __name__, url_prefix="/profile")
sc = Blueprint("shortcut", __name__, url_prefix="/shortcut")
sales = Blueprint("sales", __name__, url_prefix="/sales")
accounts = Blueprint("accounts", __name__, url_prefix="/accounts")


app.config["SECRET_KEY"] = config.HEX_SEC_KEY
# region Metodos de validacion (Posbilemente no sirva)
def validar_entrada(texto):
    # a-z y A-Z son para minusculas y mayusculas
    # \u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00c1\u00c9\u00cd\u00d3\u00da\u00d1  Letras mayusculas y minusculas con acentos
    # \s Espacios en blanco
    # '' Al menos un caracter del conjunto
    # $ Al final de la cadena
    # Definimos el patrón que NO queremos en la entrada
    patron = r"^[a-zA-Z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00c1\u00c9\u00cd\u00d3\u00da\u00d1\s]+$"

    # Buscamos si hay alguna coincidencia en el texto
    if not re.search(patron, texto):
        return False
    else:
        return True

# region ShortCut
@sc.route("/shortcut")
def shortcut():
    # Errores
    print("<#################### index ####################")
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    print("#################### FIN RenderT(index.html) ####################>")
    return render_template("shortcut.html", IsAdmin=session["ES_ADMIN"])


# region Ruta Principal
@app.route("/")
def index():
    # Errores
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return render_template("index.html")
    print("#################### FIN RenderT(index.html) ####################>")
    return redirect(url_for("shortcut.shortcut"))


# region Bienvenida (Terminado)
@p.route("/welcomeuser") 
def welcomeuser():
    # Errores
    print("<#################### welcomeuser ####################")
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    print("Session > ",session)
    print("Nombre > ",session['name'])
    print("Es admin? > ", session["ES_ADMIN"])
    print("#################### FIN (profile/welcome-user.html) ####################>")
    return render_template(
        "profile/welcome-user.html",
        user=session["name"],
        IsAdmin=session["ES_ADMIN"],
    )

# region Iniciar session (Terminado)
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    # Errores
    email_not_found = False # El correo electrónico no está registrado
    bad_password = False  # La contreaseña es incorrecta - Enviar True 
    registration_successful = False
    print("<#################### signin ####################")
    if "email" in session:
        print("#################### Email In Session ####################>")
        return render_template("profile/welcome-user.html", email=session["email"])
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print("<==================== DATOS OBTENIDOS ====================")
        print(f"Email - {email}")
        print(f"Password - {password}")
        print("========================================>")
        existing_email = config.Read(
            """
            SELECT * 
            FROM proyecto.usuarios 
            WHERE CORREO = ?
            AND proyecto.usuarios.ESTATUS = 1
            """,
            (email,),
        )
        if not existing_email:
            # El correo electrónico no está registrado
            email_not_found = True
            print(
                "#################### Renderizar auth/signin.html - Correo electrónico no está registrado ####################>"
            )
        else:
            # El correo electrónico está registrado
            if existing_email[0][6] == password:
                # Contraseña correcta
                session["email"] = existing_email[0][5]
                session["ES_ADMIN"] = bool(existing_email [0][8])
                session["name"] = f"{existing_email[0][1]} {existing_email[0][2]} {existing_email[0][3]} "
                print(
                    "#################### profile.welcomeuser - Contraseña correcta ####################>"
                )
                print("Correo > ",session["email"])
                print("Es Admin? >", session["ES_ADMIN"])
                print("user >", session["name"])
                registration_successful = True
                return redirect(
                    url_for("profile.welcomeuser")
                )
            else:
                # Contraseña incorrecta
                bad_password = True
                print(
                    "#################### Renderizar auth/signin - Contraseña incorrecta ####################>"
                )
        return render_template(
            "auth/signin.html",
            bad_password=bad_password,
            email_not_found=email_not_found,
            registration_successful=registration_successful,
        )
    print("#################### Return to auth/signin.html ####################>")
    return render_template("auth/signin.html",registration_successful=registration_successful,)


# region Registrarse (Terminado)
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # Errores
    email_found = False # El email ya esta registrado
    user_found = False  #   El usuario ya ha sido encontradoin
    ErrorNombre = False
    ErrorAP_PAT = False
    ErrorAP_MAT = False
    # Otros booleanos
    registration_successful = False
    print("<#################### signup ####################")
    # Verificar si hay una dirección de correo dentro de la sesión
    if "email" in session:
        print("#################### Session iniciada renderizar index.html ####################>")
        return render_template(
            "index.html", email=session["email"], IsAdmin=session["ES_ADMIN"]
        )
    elif request.method == "POST":
        # Obtener datos del formulario
        name = request.form.get("name")
        apellido_paterno = request.form.get("paternal_lastname")
        apellido_materno = request.form.get("maternal_lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        # Probar si el formato es correcto:
        ErrorNombre = validar_entrada(name)
        ErrorAP_PAT = validar_entrada(apellido_paterno)
        ErrorAP_MAT = validar_entrada(email)

        # Prubas
        print("<==================== DATOS OBTENIDOS ====================")
        print(f"Name - {name}")
        print(f"apellido_paterno - {apellido_paterno}")
        print(f"apellido_materno - {apellido_materno}")
        print(f"Email - {email}")
        print(f"Password - {password}")
        print("========================================>")
        print("<==================== VERIFICAR CORREO/USUARIO ====================")
        print("CONSULTA CORREO")
        # Consulta para verificar si existe el correo en la BD
        existing_email = config.Read(
            """
            SELECT * 
            FROM proyecto.usuarios 
            WHERE CORREO = ?
            """,
            (email,)
        )
        print("CONSULTA USUARIO")
        # Consulta para verificar si existe el usuario en la BD
        existing_user = config.Read(
            """
            SELECT * 
            FROM proyecto.usuarios 
            WHERE NOMBRE = ? 
            AND AP_PAT = ? 
            AND AP_MAT = ?
            """,
            (name, apellido_paterno, apellido_materno)
        )
        print("========================================>")
        # Existe el correo en la base de datos
        if existing_email:
            email_found = True
        # Existe el usuario en la base de datos
        if existing_user:
            user_found = True
        # Cualquier error
        if existing_email or existing_user:
            return render_template(
                "auth/signup.html",
                user_found=user_found,
                email_found=email_found,
            )
        # No hay ningún error
        else:
            print("<==================== REGISTRO EN BD ====================")
            # Registrar en base de datos
            config.CUD(
                """
                INSERT INTO proyecto.usuarios (NOMBRE, AP_PAT, AP_MAT, CORREO, CONTRASENA, ESTATUS, ES_ADMIN) 
                VALUES (?, ?, ?, ?, ?, 1, 0)
                """,
                (
                    name,
                    apellido_paterno,
                    apellido_materno,
                    email,
                    password,
                ),  # Tupla correctamente definida
            )
            print("========================================>")
            # Salio todo bien entonces
            registration_successful = True
            user = f"{name} {apellido_paterno} {apellido_materno} "
            print("#################### Renderizar auth/signin ####################>")
            flash(f"¡Gracias por registrarte, {user}!", "éxito")
            return render_template(
                "auth/signup.html", registration_successful=registration_successful
            )
    else:
        print("#################### Renderizar auth/signup.html ####################>")
        return render_template("auth/signup.html")


# region Cerrar session (Terminado)
@app.route("/signout")
def signout():
    print("<#################### signout ####################")
    if "email" in session:
        session.clear()
        flash("Se ha cerrado la session correctamente.")
        print("#################### FIN (auth.signin) ####################>")
        return redirect(url_for("index"))
    else:
        print("#################### FIN NO HAY SESSION (auth.signin) ####################>")
    return redirect(url_for("auth.signin"))
# endregion

# region Registro exitoso (Terminado)
@app.route("/successful_registration")
def successful_registration():
    return render_template("auth/successful-registration.html")
# endregion

# region consultas
def ConsultaProductos():
    productos = []
    productos = config.Read(
        """
        SELECT 
            ID_PRODUCTO, 
            NOMBRE, 
            PRECIO_UNITARIO, 
            EXISTENCIAS 
        FROM proyecto.almacen 
        WHERE proyecto.almacen.ESTATUS = 1
        """
    )
    return productos


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


# region Mostrar los productos (Terminado)
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
        products = config.Read(
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
        # region Caso 1: Borrar producto
        if form_type == "delete":
            product_id = int(request.form.get("product_id"))
            config.CUD(
                    "UPDATE proyecto.almacen  SET ESTATUS = 0 WHERE ID_PRODUCTO = ?",
                    (product_id,),
            )
            flash("El producto ha sido eliminado exitosamente.")
        # endregion
        # region Caso 2: Crear producto
        elif form_type == "create":
            try:
                # Obtener datos del formulario
                marca = request.form.get("marca")
                producto = request.form.get("producto")
                unit_quantity = request.form.get("unitquantity")  # Cantidad
                select_unit_quantity = request.form.get("SelectUnitOfMeasure")  # Unidad de medida

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
                    raise MyException("InvalidInput", "La cantidad debe ser un número entero válido.")

                try:
                    precio = float(request.form.get("precio"))
                except ValueError:
                    raise MyException("InvalidInput", "El precio debe ser un número válido.")

                try:
                    compania = int(request.form.get("company_id"))
                except ValueError:
                    raise MyException("InvalidInput", "El ID de la compañía debe ser un número entero válido.")

                try:
                    intermediario = int(request.form.get("intermedary_id"))
                except ValueError:
                    raise MyException("InvalidInput", "El ID del intermediario debe ser un número entero válido.")

                # Errores
                if cantidad <= 0 or precio <= 0:
                    raise MyException(
                        "NonPositive",
                        f"Los valores proporcionados {cantidad, precio} no son positivos. Deben ser mayores que cero."
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
                print("<==================== VERIFICAR RELACION COMPANIA - INTERMEDIARIO ====================")
                existe = config.Read(
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
                productoinactivo = config.Read(
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
                productoexiste = config.Read(
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
                    print("====================! Existing product in the DB.====================>")
                    raise MyException("ProductExists", "El producto existe")
                elif productoinactivo:
                    print("====================! Producto existente (Oculto) en la BD.====================>")
                    product_id = productoinactivo[0][0]
                    config.CUD(
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
                    config.CUD(
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
                    print("====================!Producto creado exitosamente.!====================>")
                    flash("Producto creado exitosamente.")
                    print("#################### FIN ####################>")
                else:
                    print("====================!La compañía o el intermediario no cumplen las condiciones necesarias.====================>")
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
        # region Caso 3: Actualizar producto
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
                existe = config.Read(
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
                productoexiste = config.Read(
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
                    config.CUD(
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

# region Manejar los intermediario (Terminado)
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
        # region Caso 1: int(id_intermediario)
        if action == "delete":
            try:
                print("<#################### delete ####################")
                id_intermediario = int(request.form.get("DeleteIntermediaryId"))#posible error en el SQL
                NoSePuedeBorrar = config.Read(
                    """
                    SELECT 
                        proyecto.almacen.NOMBRE
                    FROM proyecto.intermediario,proyecto.Almacen
                    WHERE proyecto.intermediario.ID_INTERMEDIARIO = proyecto.Almacen.ID_INTERMEDIARIO
                    AND proyecto.almacen.EXISTENCIAS != 0
                    AND proyecto.intermediario.ID_INTERMEDIARIO = ?
                    """,
                    (id_intermediario,)
                )
                if NoSePuedeBorrar:
                    raise MyException(
                        "Error al borrar compañia.",
                        "Para poder borrar un intermediario primero debe asegurarse que los productos relacionados sean inexistentes.",
                    )
                config.CUD(
                    """
                    -- Actualizar proyecto.Almacen
                    UPDATE proyecto.almacen
                    SET ESTATUS = 0
                    WHERE ID_INTERMEDIARIO = ?;
                    """,
                    (int(id_intermediario),),
                )
                config.CUD(
                    """
                    -- Actualizar proyecto.intermediario
                    UPDATE proyecto.intermediario
                    SET ESTATUS = 0
                    WHERE ID_INTERMEDIARIO = ?;
                    """,
                    (
                        int(id_intermediario),
                    ),
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
                VerificarInactivo = config.Read(
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
                existe = config.Read(
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
                tel_existe = config.Read(
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
                    config.CUD(
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
                    config.CUD(
                            """
                            INSERT INTO proyecto.intermediario (NOMBRE, AP_PAT, AP_MAT, TEL, ESTATUS, ID_COMPANIA) 
                            VALUES (?, ?, ?, ?, 1, ?)
                            """,
                            (nombre, apellido_paterno, apellido_materno, int(telefono), int(company_id)),
                        )
                    print("#################### FIN (Se inserto en la BD) ####################>")
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto) ####################>")
            except Exception as e:
                print(f"Type : {e}")
                flash(f"{e}")
                print("#################### FIN (No se inserto) ####################>")
        elif action == "edit":
            try:
                # Obtener datos del formulario, incluido company_id
                nombre = request.form.get("editIntermediaryName")
                apellido_paterno = request.form.get("NEW-AP_PAT")
                apellido_materno = request.form.get("NEW-AP_MAT")
                telefono = int(request.form.get("editIntermediaryPhone"))
                company_id = int(request.form.get("Edit-company_id"))
                id_intermediario = int(request.form.get(
                    "EditIntermediary_id"
                ) ) # Se obtiene de un dato oculto
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
                existe = config.Read(
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
                tel_existe = config.Read(
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
                    config.CUD(
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
                    flash("Se ha actualizado correctamente los datos del intermediario.")
                    print("Se ha actualizado correctamente los datos del intermediario.")
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
    # Datos que se envian siempre
    relations = []
    relations = config.Read(
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

# Manejar COMPAÑIA (Terminado)
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
        if action == "delete":
            try:
                print("<#################### delete ####################")
                id_intermediario = int(request.form.get("DeleteIntermediaryId"))#cambiar la direccion 
                NoSePuedeBorrar = config.Read(
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
                config.CUD(
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
                config.CUD(
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
                config.CUD(
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
        elif action == "create":
            try:
                # Obtener datos del formulario
                nombre = request.form.get("companyName")
                # Pruebas
                print("<==================== DATOS OBTENIDOS ====================")
                print(f"Nombre: {nombre}")
                print("========================================>")
                # Existe pero esta inactivo
                VerificarInactivo = config.Read(
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
                # Verificar si la compañia ya existe
                existe = config.Read(
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
                    config.CUD(
                            """
                            UPDATE proyecto.proveedor
                            SET ESTATUS=1
                            WHERE ID_COMPANIA = ?
                            """,
                            (
                                
                                VerificarInactivo[0][0],
                            ),
                        )
                else:
                    # Insertar en la base de datos si no hay errores
                    config.CUD(
                            """
                            INSERT INTO proyecto.proveedor (NOMBRE,  ESTATUS) 
                            VALUES (?, 1)
                            """,
                            (nombre,),
                        )
                    print("#################### FIN (Se inserto en la BD) ####################>")
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto) ####################>")
            except Exception as e:
                print(f"Type : {e}")
                flash(f"Type : {e}")
                print("#################### FIN (No se inserto) ####################>")
        elif action == "edit":
            try:
                # Obtener datos del formulario, incluido company_id
                nombre = request.form.get("editcompanyName")
                id_intermediario = int(request.form.get(
                    "EditIntermediary_id"
                ) )
                # Pruebas
                print("<==================== DATOS OBTENIDOS ====================")
                print(f"nombre - {nombre}")
                print(f"id-company - {id_intermediario}")
                print("========================================>")
                # Verificar si es inactivo
                ExisteInactivo = config.Read(
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
                existe = config.Read(
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
                    config.CUD(
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
    # Datos que se envian siempre
    relations = []
    relations = config.Read(
        """
        SELECT 
            proyecto.proveedor.ID_COMPANIA,
            proyecto.proveedor.NOMBRE
        FROM proyecto.proveedor 
        WHERE proyecto.proveedor.ESTATUS = 1 
        """
    )
    return render_template(
        "products/manage-company.html",
        relations=relations,
        companies=ConsultaCompanias(),
        IsAdmin=session["ES_ADMIN"],
    )

# Agregar Ventas
@sales.route("/addsalesworker", methods=["GET", "POST"])
def addsalesworker():
    # Errores
    ErrorCantidad = False
    ErrorPrecio = False
    ErrorProductoInexistente = False
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
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
                ExisteProducto = config.Read(
                    """
                    SELECT 
                        proyecto.almacen.ID_PRODUCTO,
                        proyecto.almacen.PRECIO_UNITARIO,
                        proyecto.almacen.EXISTENCIAS
                    FROM proyecto.almacen 
                    WHERE proyecto.almacen.ESTATUS = 1 
                    AND proyecto.almacen.ID_PRODUCTO = ?
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
                    config.Read(
                    """
                    SELECT proyecto.dia.ID_DIA 
                    FROM proyecto.dia 
                    WHERE proyecto.dia.DIA = ?
                    """,
                        (DiaA,),)[0][0]
                )
                # Encontrar ID_MES en BD MES
                print("Paso 1: Encontrar ID_MES en BD MES")
                Mes = int(
                    config.Read(
                    """
                    SELECT proyecto.mes.ID_MES 
                    FROM proyecto.mes 
                    WHERE proyecto.mes.MES = ?
                    """,
                        (MesA,),
                    )[0][0]
                )
                # Encontrar ID_ANIO en BD ANIO
                print("Paso 1: Encontrar ID_ANIO en BD ANIO")
                Anio = int(
                    config.Read(
                    """
                    SELECT proyecto.anio.ID_ANIO 
                    FROM proyecto.anio 
                    WHERE proyecto.anio.ANIO = ?
                    """,
                        (AnioA,),
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
                        Cost = (tabla[i][1]) * (Entrada[i][1])  # Costo por producto
                        IvaValue = Cost * 0.16  # Asumiendo que el IVA es del 16%
                        SumaCosto += Cost  # Sumar los costos por producto
                        SumaIva += round(IvaValue) # Sumar los iva por producto
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
                    config.CUD(
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
                    id = int(config.Read("SELECT LAST_INSERT_ID() AS NewID;")[0][0])
                    #
                    print("ID-VENTA>", id)
                    for y in range(len(TablaDetalles)):
                        config.CUD(
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
                        config.CUD(
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
                                int(tabla[i][1] * (tabla[z][2] - Entrada[z][1])),
                                ESTATUS,
                                int(tabla[z][0]),
                            ),
                        )
        except Exception as e:
            print(e)
    # Siempre se envia estos datos
    products = config.Read(
        """
                SELECT 
                    ID_PRODUCTO, 
                    NOMBRE, 
                    PRECIO_UNITARIO, 
                    EXISTENCIAS,
                    ESTATUS
                FROM proyecto.almacen 
                WHERE proyecto.almacen.ESTATUS = 1
                """
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
        IsAdmin=session["ES_ADMIN"]
    )


@sales.route("/reportsales", methods=["POST","GET"])
def reportsales():
    print("<#################### reportsales ####################")
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    # Capa 2: Verificar si el usuario es administrador
    if not session.get("ES_ADMIN"):
        print("#################### NO ES ADMIN ####################>")
        return redirect(url_for("shortcut.shortcut"))
    # Capa 3: Procesar la solicitud POST
    if request.method == "POST":
        sale_id = request.form.get("sale_id")
        details = config.Read(
            """
            SELECT proyecto.detalles.ID_PRODUCTO, proyecto.almacen.NOMBRE, proyecto.detalles.CANTIDAD, proyecto.detalles.IMPORTE, proyecto.detalles.IVA
            FROM proyecto.almacen, proyecto.detalles
            WHERE proyecto.almacen.ID_PRODUCTO = proyecto.detalles.ID_PRODUCTO
            AND proyecto.detalles.ID_VENTA = ?
            """,
            (sale_id,),
        )
        sales = config.Read(
            """
            SELECT 
                proyecto.ventas.ID_VENTA, 
                proyecto.dia.DIA, 
                proyecto.mes.MES, 
                proyecto.anio.ANIO, 
                proyecto.ventas.CANTIDAD_VENTA, 
                proyecto.ventas.TOTAL
            FROM proyecto.ventas, proyecto.dia, proyecto.mes, proyecto.anio
            WHERE proyecto.ventas.ID_DIA = proyecto.dia.ID_DIA
            AND proyecto.ventas.ID_MES = proyecto.mes.ID_MES
            AND proyecto.ventas.ID_ANIO = proyecto.anio.ID_ANIO
            """
        )
        return render_template("sales/report-sales.html", sales=sales, details=details,IsAdmin=session["ES_ADMIN"])

    # Capa 4: Obtener todas las ventas si no hay método POST
    print("<==================== DATOS OBTENIDOS ====================")
    sales = config.Read(
        """
        SELECT 
            proyecto.ventas.ID_VENTA, 
            proyecto.dia.DIA, 
            proyecto.mes.MES, 
            proyecto.anio.ANIO, 
            proyecto.ventas.CANTIDAD_VENTA, 
            proyecto.ventas.TOTAL
        FROM proyecto.ventas, proyecto.dia, proyecto.mes, proyecto.anio
        WHERE proyecto.ventas.ID_DIA = proyecto.dia.ID_DIA
        AND proyecto.ventas.ID_MES = proyecto.mes.ID_MES
        AND proyecto.ventas.ID_ANIO = proyecto.anio.ID_ANIO
        """
    )
    print(f"products > {sales}")
    print("========================================>")
    print(
        "#################### FIN RenderT(products/warehouse.html) ####################>"
    )
    return render_template(
        "sales/report-sales.html", sales=sales, IsAdmin=session["ES_ADMIN"]
    )

# Manejar las cuentas (test)
@accounts.route("/manage_accounts", methods=["GET", "POST"])
def manage_accounts():
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
        if action == "delete":
            try:
                print("<#################### delete ####################")
                id_intermediario = int(request.form.get("DeleteIntermediaryId"))
                print(f"id para eliminar usuarios - {id_intermediario}")
                config.CUD(
                    """
                    -- Actualizar proyecto.usuarios
                    UPDATE proyecto.usuarios
                    SET ESTATUS = 0
                    WHERE ID_USUARIO = ?;
                    """,
                    (int(id_intermediario),),
                )
            except Exception as e:
                print(f"Type : {e}")
                flash(f"Type : {e}")
                print(
                    "#################### FIN (Error al borrar intermediario) ####################>"
                )
        elif action == "edit":
            try:
                # Obtener datos del formulario, incluido company_id
                nombre = request.form.get("editIntermediaryName")
                apellido_paterno = request.form.get("NEW-AP_PAT")
                apellido_materno = request.form.get("NEW-AP_MAT")
                correo = request.form.get("NEW-Correo")
                id_usuario = int(
                    request.form.get("EditIntermediary_id")
                )  # Se obtiene de un dato oculto
                # Pruebas
                print("<==================== DATOS OBTENIDOS ====================")
                print(f"nombre - {nombre}")
                print(f"apellido_paterno - {apellido_paterno}")
                print(f"apellido_materno - {apellido_materno}")
                print(f"correo - {correo}")
                print(f"id_usuario - {id_usuario}")
                print("========================================>")
                # Consulta para verificar si existe el correo en la BD
                existing_email = config.Read(
                    """
                    SELECT * 
                    FROM proyecto.usuarios 
                    WHERE proyecto.usuarios.CORREO = ?
                    AND proyecto.usuarios.ID_USUARIO != ?
                    """,
                    (correo, int(id_usuario)),
                )
                # Consulta para verificar si existe el usuario en la BD
                existing_user = config.Read(
                    """
                    SELECT * 
                    FROM proyecto.usuarios 
                    WHERE proyecto.usuarios.NOMBRE = ?
                    AND proyecto.usuarios.AP_PAT = ?
                    AND proyecto.usuarios.AP_MAT= ?
                    AND proyecto.usuarios.ID_USUARIO != ?
                    """,
                    (nombre, apellido_paterno, apellido_materno, int(id_usuario)),
                )
                # Cualquier error
                if existing_email or existing_user:
                    if existing_email and existing_user:
                        raise MyException(
                            "ErrorEditAccounts",
                            "El correo electronico y usuario ya existe en la base de datos.",
                        )
                    elif existing_email:
                        raise MyException(
                            "ErrorEditAccounts",
                            "El correo electronico ya existe en la base de datos.",
                        )
                    elif existing_user:
                        raise MyException(
                            "ErrorEditAccounts",
                            "El usuario ya existe en la base de datos.",
                        )
                else:
                    # Actualizar en la base de datos
                    config.CUD(
                        """
                        UPDATE proyecto.usuarios 
                        SET NOMBRE=?, AP_PAT=?, AP_MAT=?, CORREO=?
                        WHERE ID_USUARIO = ?
                        """,
                        (
                            nombre,
                            apellido_paterno,
                            apellido_materno,
                            correo,
                            int(id_usuario),
                        ),
                    )
                    flash("Se ha actualizado correctamente los datos.")
                    print("Se ha actualizado correctamente los datos.")
                    print("#################### FIN ####################>")
            except MyException as ex:
                Tipo, Mensaje = ex.args
                print(f"Type {Tipo} : {Mensaje}")
                flash(f"{Mensaje}")
                print("#################### FIN (No se inserto F) ####################>")
            except Exception as e:
                print(f"Type : {e}")
                flash(f"{e}")
                print("#################### FIN (No se inserto FX2) ####################>")
    # Datos que se envian siempre
    relations = []
    relations = config.Read(
        """
        SELECT 
            proyecto.usuarios.ID_USUARIO,
            proyecto.usuarios.NOMBRE,
            proyecto.usuarios.AP_PAT,
            proyecto.usuarios.AP_MAT,
            proyecto.usuarios.CORREO 
        FROM proyecto.usuarios 
        WHERE proyecto.usuarios.ESTATUS = 1 
        AND proyecto.usuarios.ES_ADMIN = 0
        """
    )
    print(
        "#################### products/manage-intermediary.html ####################>"
    )
    return render_template(
        "accounts/manage-accounts.html",
        relations=relations,
        companies=ConsultaCompanias(),
        IsAdmin=session["ES_ADMIN"],
    )

# Ajuste de perfil (En Desarrollo)
@p.route("/profile")
def profile():
    return render_template("profile/profile.html")


# Ajustes (En Desarrollo)
@sc.route("/settings")
def settings():
    return render_template("settings/settings.html")


# Registrar los Blueprints en la App
app.register_blueprint(auth)
app.register_blueprint(products)
app.register_blueprint(p)
app.register_blueprint(sc)
app.register_blueprint(sales)
app.register_blueprint(accounts)


# Ruta dinámica para archivos estáticos
@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(debug=True, port=8000)

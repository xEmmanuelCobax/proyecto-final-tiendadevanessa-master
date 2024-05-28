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


app.config["SECRET_KEY"] = config.HEX_SEC_KEY
# Metodos de validacion:
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

# ShortCut
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


# Ruta Principal
@app.route("/")
def index():
    # Errores
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return render_template("index.html")
    print("#################### FIN RenderT(index.html) ####################>")
    return redirect(url_for("shortcut.shortcut"))


# Bienvenida (Terminado)
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

# Iniciar session (Terminado)
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    # Errores
    
    email_not_found = False # El correo electrónico no está registrado
    bad_password = False  # La contreaseña es incorrecta - Enviar True 
    # Datos a usar: 
    """
    1- Email 
    2- Password
    3-
    4-
    5-
    """
    registration_successful = request.args.get('registration_successful', 'False')

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
            FROM dbo.Usuarios 
            WHERE CORREO = ?
            AND dbo.Usuarios.ESTATUS = 1
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


# Registrarse (Terminado)
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
    # Datos a usar:
    """
    1- name>
    2- apellido_paterno>
    3- apellido_materno>
    4- email
    5- password
    """
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
        # Consulta para verificar si existe el correo en la BD
        existing_email = config.Read(
            """
            SELECT * 
            FROM dbo.Usuarios 
            WHERE CORREO = ?
            """,
            email,
        )
        # Consulta para verificar si existe el usuario en la BD
        existing_user = config.Read(
            """
            SELECT * 
            FROM dbo.Usuarios 
            WHERE NOMBRE = ? 
            AND AP_PAT = ? 
            AND AP_MAT = ?
            """,
            (name, apellido_paterno, apellido_materno)
        )
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
            # Registrar en base de datos
            config.CUD(
                """
                INSERT INTO dbo.Usuarios (NOMBRE, AP_PAT, AP_MAT, CORREO, CONTRASENA, ESTATUS) 
                VALUES (?, ?, ?, ?, ?, 1)
                """,
                (name, apellido_paterno, apellido_materno, email, password),
            )
            # Salio todo bien entonces
            registration_successful = True
            user = f"{name} {apellido_paterno} {apellido_materno} "
            print("#################### Renderizar auth/signin ####################>")
            return redirect(url_for("auth.signin", registration_successful=registration_successful))
            # return render_template(
            #     "auth/signin.html",
            #     registration_successful=registration_successful,
            #     user=user,
            # )
    else:
        print("#################### Renderizar auth/signup.html ####################>")
        return render_template("auth/signup.html")


# Cerrar session (Terminado)
@app.route("/signout")
def signout():
    print("<#################### signout ####################")
    if "email" in session:
        session.clear()
        print("#################### FIN (auth.signin) ####################>")
        return redirect(url_for("index"))
    else:
        print("#################### FIN NO HAY SESSION (auth.signin) ####################>")
    return redirect(url_for("auth.signin"))


# Registro exitoso (Terminado)
@app.route("/successful_registration")
def successful_registration():
    return render_template("auth/successful-registration.html")


def ConsultaProductos():
    productos = []
    productos = config.Read(
        """
        SELECT 
            ID_PRODUCTO, 
            NOMBRE, 
            PRECIO_UNITARIO, 
            EXISTENCIAS 
        FROM dbo.Almacen 
        WHERE dbo.Almacen.ESTATUS = 1
        """
    )
    return productos


def ConsultaPIA():
    Cpia = []
    Cpia = config.Read(
        """
    SELECT 
        dbo.Almacen.ID_PRODUCTO,
        dbo.Almacen.NOMBRE, 
        dbo.Almacen.PRECIO_UNITARIO, 
        dbo.Almacen.EXISTENCIAS,
        dbo.Almacen.PRECIO_EXISTENCIA, 
        dbo.Intermediario.NOMBRE,
        dbo.Intermediario.AP_PAT,
        dbo.Intermediario.AP_MAT,
        dbo.Intermediario.TEL,
        dbo.Proveedor.NOMBRE
    FROM dbo.Proveedor, dbo.Intermediario, dbo.Almacen
    WHERE dbo.Proveedor.ID_COMPANIA = dbo.Intermediario.ID_COMPANIA
    AND dbo.Intermediario.ID_INTERMEDIARIO = dbo.Almacen.ID_INTERMEDIARIO
    AND dbo.Almacen.ESTATUS = 1
        """
    )
    return Cpia


def ConsultaIntermediarios():
    Intermediarios = []
    Intermediarios = config.Read(
        """
        SELECT 
            dbo.Proveedor.ID_COMPANIA,
            dbo.Proveedor.NOMBRE,
            dbo.Intermediario.ID_INTERMEDIARIO,
            dbo.Intermediario.NOMBRE, 
            dbo.Intermediario.AP_PAT, 
            dbo.Intermediario.AP_MAT 
        FROM dbo.Proveedor 
        INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA 
        WHERE dbo.Proveedor.ESTATUS = 1 
        AND dbo.Intermediario.ESTATUS = 1;
        """
    )
    return Intermediarios


def ConsultaCompanias():
    companias = []
    companias = config.Read(
        """
        SELECT 
            dbo.Proveedor.ID_COMPANIA, 
            dbo.Proveedor.NOMBRE  
        FROM dbo.Proveedor  
        WHERE dbo.Proveedor.ESTATUS = 1 ;
        """
    )
    return companias


# Mostrar los productos (Terminado)
@products.route("/warehouse")
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


# Buscar producto (Terminado)
@products.route("/search_product", methods=["GET", "POST"])
def search_product():
    print("<#################### search_product ####################")
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
        search_term = (str(request.form.get("search_term"))).strip()
        # Pruebas
        print("<==================== DATOS OBTENIDOS ====================")
        print(f"nombre - {search_term}")
        print("========================================>")
        # Consulta
        products = config.Read(
            """
                        SELECT 
                            dbo.Almacen.ID_PRODUCTO,
                            dbo.Almacen.NOMBRE, 
                            dbo.Almacen.PRECIO_UNITARIO, 
                            dbo.Almacen.EXISTENCIAS 
                        FROM  dbo.Almacen 
                        WHERE NOMBRE LIKE ?
                        AND dbo.Almacen.ESTATUS = 1;
                        """,
            ("%" + search_term + "%",),
        )
        print(
            "#################### FIN RenderT(products/warehouse.html) ####################>"
        )
    return render_template(
        "products/warehouse.html", products=products, IsAdmin=session["ES_ADMIN"]
    )


# Manejar el inventario (Terminado)
@products.route("/manage_warehouse", methods=["GET", "POST"])
def managewarehouse():
    print("<#################### manage_warehouse ####################")
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    # Capa 2: Verificar si el usuario es administrador
    if not session.get("ES_ADMIN"):
        print("#################### NO ES ADMIN ####################>")
        return redirect(url_for("shortcut.shortcut"))
    # Capa 3: Manejar los parámetros de error y caso
    OtrosErroresBorrarProducto = request.args.get("OtrosErroresBorrarProducto")
    OtrosErroresCrearProducto = request.args.get("OtrosErroresCrearProducto")
    OtrosErroresActualizarProducto = request.args.get("OtrosErroresActualizarProducto")
    ErrorCantidad = request.args.get("ErrorCantidad")
    ErrorPrecio = request.args.get("ErrorPrecio")
    ErrorProductoExiste = request.args.get("ErrorProductoExiste")
    ErrorRelacion = request.args.get("ErrorRelacion")
    CasoActivarProducto = request.args.get("CasoActivarProducto")

    print("<==================== DATOS OBTENIDOS ====================")
    # Errores no contemplados
    print("OtrosErroresBorrarProducto > ", OtrosErroresBorrarProducto)
    print("OtrosErroresCrearProducto > ", OtrosErroresCrearProducto)
    print("OtrosErroresActualizarProducto > ", OtrosErroresActualizarProducto)
    # Errores
    print("ErrorCantidad > ", ErrorCantidad)
    print("ErrorPrecio > ", ErrorPrecio)
    print("ErrorProductoExiste > ", ErrorProductoExiste)
    print("ErrorRelacion > ", ErrorRelacion)
    # Casos
    print("CasoActivarProducto > ", CasoActivarProducto)
    print("========================================>")
    print(
        "#################### FIN RenderT(products/manage-warehouse.html) ####################>"
    )
    # Renderizar la plantilla con los datos obtenidos y los errores/casos
    return render_template(
        "products/manage-warehouse.html",
        products=ConsultaPIA(),
        relations=ConsultaIntermediarios(),
        companies=ConsultaCompanias(),
        OtrosErroresBorrarProducto=OtrosErroresBorrarProducto,
        OtrosErroresCrearProducto=OtrosErroresCrearProducto,
        OtrosErroresActualizarProducto=OtrosErroresActualizarProducto,
        ErrorCantidad=ErrorCantidad,
        ErrorPrecio=ErrorPrecio,
        ErrorProductoExiste=ErrorProductoExiste,
        ErrorRelacion=ErrorRelacion,
        CasoActivarProducto=CasoActivarProducto,
        IsAdmin=session["ES_ADMIN"],
    )


# Borrar producto (Terminado)
@products.route("/delete_product", methods=["POST"])
def delete_product():
    # Errores
    print("<#################### delete_product ####################")
    OtrosErroresBorrarProducto = False
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
        try:
            # Obtener el ID del producto de los datos del formulario
            product_id = int(request.form.get("product_id"))
            print("<==================== DATOS OBTENIDOS ====================")
            print(f"Product_ID - {product_id}")
            print("========================================>")
            config.CUD(
                """
                UPDATE dbo.Almacen 
                SET 
                    ESTATUS = 0 
                WHERE ID_PRODUCTO = ?
                """,
                (product_id,),
            )
            print("#################### FIN ####################>")
        except Exception as e:
            OtrosErroresBorrarProducto = True
        return redirect(
            url_for(
                "products.managewarehouse",
                OtrosErroresBorrarProducto=OtrosErroresBorrarProducto,
            )
        )

# Crear producto (Terminado)
@products.route("/create_product", methods=["POST"])
def create_product():
    # Errores
    ErrorCantidad = False
    ErrorPrecio = False
    ErrorProductoExiste = False
    ErrorRelacion = False
    OtrosErroresCrearProducto = False
    CasoActivarProducto = False
    print("<#################### create_product ####################")
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
        try:
            # Obtener datos del formulario
            marca = request.form.get("marca")
            producto = request.form.get("producto")
            # Unidad de medida
            unit_quantity = int(request.form.get("unitquantity"))  # Cantidad
            seslect_unit_quantity = request.form.get(
                "SelectUnitOfMeasure"
            )  # Unidad de medida
            # Construir la cantidad con la unidad de medida
            if seslect_unit_quantity == "pieces":
                quantity = str(unit_quantity) + "Pzs"
            elif seslect_unit_quantity == "liters":
                quantity = str(unit_quantity) + "l"
            elif seslect_unit_quantity == "milliliters":
                quantity = str(unit_quantity) + "ml"
            elif seslect_unit_quantity == "kilogram":
                quantity = str(unit_quantity) + "kg"
            elif seslect_unit_quantity == "grams":
                quantity = str(unit_quantity) + "gr"
            else:
                quantity = str(unit_quantity) + "custom"
            # Datos formados
            nombre = f"{marca}_{producto}_{quantity}"
            cantidad = int(request.form.get("cantidad"))
            precio = float(request.form.get("precio"))
            compania = int(request.form.get("company_id"))
            intermediario = int(request.form.get("intermedary_id"))
            # Errores
            if cantidad <= 0 or precio <= 0:
                if cantidad <= 0 or precio <= 0:
                    ErrorCantidad = True
                    ErrorPrecio = True
                    raise MyException(
                        "NonPositive",
                        f"Los valores proporcionados {cantidad,precio} no son positivos. Debem ser mayor que cero.",
                    )
                elif cantidad <= 0:
                    ErrorCantidad = True
                    raise MyException(
                        "NonPositive",
                        f"El valor proporcionado {cantidad} no es positivo. Debe ser mayor que cero.",
                    )
                elif precio <= 0:
                    ErrorPrecio = True
                    raise MyException(
                        "NonPositive",
                        f"El valor proporcionado {precio} no es positivo. Debe ser mayor que cero.",
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
                (int(intermediario), int(compania)),
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
                ErrorProductoExiste = True
                raise MyException(
                    "ProductExists",
                    "El producto existe",
                )
            elif productoinactivo:
                print(
                    "====================! Producto existente (Oculto) en la BD.====================>"
                )
                CasoActivarProducto = True
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
                        float(precio),
                        int(cantidad),
                        float((precio) * (cantidad)),
                        int(intermediario),
                        int(product_id),
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
                        float(precio),
                        int(cantidad),
                        float((precio) * (cantidad)),
                        int(intermediario),
                    ),
                )
                print(
                    "====================!Producto creado exitosamente.!====================>"
                )
                flash("Producto creado exitosamente.")
                print("#################### FIN ####################>")
            else:
                # Si la compañía o el intermediario no cumplen las condiciones, redireccionar con un mensaje de error
                print(
                    "====================!La compañía o el intermediario no cumplen las condiciones necesarias.====================>"
                )
                ErrorRelacion = True
                raise MyException(
                    "CIConditions",
                    "La compañia o el intermediario no cumplen con las condiciones necesarias.",
                )
        except ValueError as e:
            print(f"ValueError: {e}")
        except MyException as ex:
            Tipo, Mensaje = ex.args
            print(f"Type: {Tipo} , {Mensaje}")
            print("#################### FIN ####################>")
        except Exception as err:
            print(f"Inesperado {err=}, {type(err)=}")
            print("#################### FIN ####################>")
        return redirect(
            url_for(
                "products.managewarehouse",
                OtrosErroresCrearProducto=OtrosErroresCrearProducto,
                ErrorCantidad=ErrorCantidad,
                ErrorPrecio=ErrorPrecio,
                ErrorProductoExiste=ErrorProductoExiste,
                ErrorRelacion=ErrorRelacion,
                CasoActivarProducto=CasoActivarProducto,
            )
        )


# Actualizar producto (Terminado)
@products.route("/update_product", methods=["POST"])
def update_product() :
    # Errores
    ErrorCantidad = False
    ErrorPrecio = False
    ErrorProductoExiste = False
    ErrorRelacion = False
    OtrosErroresActualizarProducto = False
    print("<#################### update_product ####################")
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
            # Datos formados
            nombre = f"{marca}_{producto}_{quantity}"
            cantidad = int(request.form.get("newcantidad"))
            precio = float(request.form.get("newprecio"))
            compania = int(request.form.get("company-new-select"))
            intermediario = int(request.form.get("intermedary-new-select"))
            # Errores
            if cantidad <= 0 or precio <= 0:
                if cantidad <= 0 or precio <= 0:
                    ErrorCantidad = True
                    ErrorPrecio = True
                    raise MyException(
                        "NonPositive",
                        f"Los valores proporcionados {cantidad,precio} no son positivos. Debem ser mayor que cero.",
                    )
                elif cantidad <= 0:
                    ErrorCantidad = True
                    raise MyException(
                        "NonPositive",
                        f"El valor proporcionado {cantidad} no es positivo. Debe ser mayor que cero.",
                    )
                elif precio <= 0:
                    ErrorPrecio = True
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
                        ID_INTERMEDIARIO,
                        Intermediario.NOMBRE,   
                        Intermediario.AP_PAT, 
                        Intermediario.AP_MAT, 
                        Proveedor.ID_COMPANIA, 
                        Proveedor.NOMBRE
                    FROM dbo.Proveedor
                    INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA 
                    WHERE dbo.Proveedor.ESTATUS = 1 
                    AND dbo.Intermediario.ESTATUS = 1 
                    AND dbo.Intermediario.ID_INTERMEDIARIO = ?
                    AND dbo.Proveedor.ID_COMPANIA = ?
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
                        dbo.Almacen.NOMBRE 
                    FROM dbo.Almacen 
                    WHERE dbo.Almacen.NOMBRE = ?
                    AND dbo.Almacen.ID_PRODUCTO != ?
                    AND dbo.Almacen.ESTATUS = 1
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
                ErrorProductoExiste = True
                raise MyException(
                    "ProductExists",
                    "El producto existe",
                )
            elif not existe:
                # Si la compañía o el intermediario no cumplen las condiciones, redireccionar con un mensaje de error
                print(
                    "====================! La compañía o el intermediario no cumplen las condiciones necesarias.====================>"
                )
                ErrorRelacion = True
                raise MyException(
                    "CIConditions",
                    "La compañia o el intermediario no cumplen con las condiciones necesarias.",
                )
            else:
                # Actualizar el producto en la base de datos
                config.CUD(
                    """
                        UPDATE dbo.Almacen 
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
        except ValueError as e:
            print(f"ValueError: {e}")
            flash(f"Error: {e}")
        except MyException as ex:
            Tipo, Mensaje = ex.args
            print(f"Type {Tipo} : {Mensaje}")
            flash(f"Type {Tipo} : {Mensaje}")
            print("#################### FIN ####################>")
        except Exception as e:
            print(f"Type: {e}")
            flash(f"Type: {e}")
            print("#################### FIN ####################>")
        return redirect(
            url_for(
                "products.managewarehouse",
                OtrosErroresActualizarProducto=OtrosErroresActualizarProducto,
                ErrorCantidad=ErrorCantidad,
                ErrorPrecio=ErrorPrecio,
                ErrorProductoExiste=ErrorProductoExiste,
                ErrorRelacion=ErrorRelacion,
            )
        )


# Manejar los intermediario (Terminado)
@products.route("/manage_intermediary")
def manage_intermediary():
    # Errores
    OtrosErroresBorrarIntermediario=request.args.get('OtrosErroresBorrarIntermediario')
    OtrosErroresCrearIntermediario=request.args.get('OtrosErroresCrearIntermediario')
    OtrosErroresEditarIntermediario=request.args.get('OtrosErroresEditarIntermediario')
    ErrorIntermediarioTelefono=request.args.get('ErrorIntermediarioTelefono')
    ErrorIntermediarioRegistrado=request.args.get('ErrorIntermediarioRegistrado')
    # Casos
    CasoActualizarIntermediario = request.args.get("CasoActualizarIntermediario")
    print("<#################### create_product ####################")
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    # Capa 2: Verificar si el usuario es administrador
    if not session.get("ES_ADMIN"):
        print("#################### NO ES ADMIN ####################>")
        return redirect(url_for("shortcut.shortcut"))
    # Capa 3: Manejar la lógica del formulario POST
    relations = []
    relations = config.Read(
        """
        SELECT 
            dbo.Proveedor.ID_COMPANIA,
            dbo.Proveedor.NOMBRE,
            dbo.Intermediario.ID_INTERMEDIARIO,
            dbo.Intermediario.NOMBRE, 
            dbo.Intermediario.AP_PAT,
            dbo.Intermediario.AP_MAT, 
            dbo.Intermediario.TEL 
        FROM dbo.Proveedor 
        INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA 
        WHERE dbo.Proveedor.ESTATUS = 1 
        AND dbo.Intermediario.ESTATUS = 1
        """
    )

    print("<==================== ERRORES Y CASOS ====================")
    # Errores no contemplados
    print("OtrosErroresBorrarIntermediario > ", OtrosErroresBorrarIntermediario)
    print("OtrosErroresCrearProducto > ", OtrosErroresCrearIntermediario)
    print("OtrosErroresActualizarProducto > ", OtrosErroresEditarIntermediario)
    # Errores
    print("ErrorIntermediarioTelefono > ", ErrorIntermediarioTelefono)
    print("ErrorIntermediarioRegistrado > ", ErrorIntermediarioRegistrado)
    # Casos
    print("CasoActualizarIntermediario > ", CasoActualizarIntermediario)
    print("========================================>")
    print(
        "#################### products/manage-intermediary.html ####################>"
    )
    return render_template(
        "products/manage-intermediary.html",
        relations=relations,
        companies=ConsultaCompanias(),
        OtrosErroresBorrarIntermediario=OtrosErroresBorrarIntermediario,
        OtrosErroresCrearIntermediario=OtrosErroresCrearIntermediario,
        OtrosErroresEditarIntermediario=OtrosErroresEditarIntermediario,
        ErrorIntermediarioTelefono=ErrorIntermediarioTelefono,
        ErrorIntermediarioRegistrado=ErrorIntermediarioRegistrado,
        CasoActualizarIntermediario=CasoActualizarIntermediario,
        IsAdmin=session["ES_ADMIN"],
    )


# Borrar intermediarios (Terminado)
@products.route("/delete_intermediary", methods=["POST"])
def delete_intermediary():
    # Errores
    OtrosErroresBorrarIntermediario = False
    print("<#################### delete_company ####################")
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
        try:
            # Obtener el ID del intermediario de los datos del formulario
            id_intermediario = int(
                request.form.get("DeleteIntermediaryId")
            )  # Se obtiene de un dato oculto
            print("<==================== DATOS OBTENIDOS ====================")
            print(f"company_id - {id_intermediario}")
            print("========================================>")
            config.CUD(
                """
                    UPDATE dbo.Intermediario SET ESTATUS = 0 WHERE ID_INTERMEDIARIO = ?;
                    """,
                (int(id_intermediario),),
            )
            print("#################### FIN ####################>")
        except Exception as e:
            print(f"Type : {e}")
            flash(f"Type : {e}")
            print("#################### FIN (Error) ####################>")
        return redirect(
            url_for(
                "products.manage_intermediary",
                OtrosErroresBorrarIntermediario=OtrosErroresBorrarIntermediario,
            )
        )


# Crear intermediario (Terminado)
@products.route("/create_intermediary", methods=["POST"])
def create_intermediary():
    # Errores
    ErrorIntermediarioTelefono = False
    ErrorIntermediarioRegistrado = False
    OtrosErroresCrearIntermediario = False
    CasoActualizarIntermediario = False
    print("<#################### create_company ####################")
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
            # Existe pero esta inactivo
            VerificarInactivo = config.Read(
                    """
                    SELECT 
                        dbo.Intermediario.ID_INTERMEDIARIO,
                        dbo.Intermediario.NOMBRE,
                        dbo.Intermediario.AP_PAT,
                        dbo.Intermediario.AP_MAT
                    FROM dbo.Intermediario 
                    WHERE dbo.Intermediario.NOMBRE = ?
                    AND dbo.Intermediario.AP_PAT = ?
                    AND dbo.Intermediario.AP_MAT = ?
                    AND dbo.Intermediario.ESTATUS = 0
                    """,
                    (nombre, apellido_paterno, apellido_materno),
                )
            # Verificar si el intermediario ya existe
            existe = config.Read(
                    """
                    SELECT 
                        dbo.Intermediario.NOMBRE,
                        dbo.Intermediario.AP_PAT,
                        dbo.Intermediario.AP_MAT
                    FROM dbo.Intermediario 
                    WHERE dbo.Intermediario.NOMBRE = ?
                    AND dbo.Intermediario.AP_PAT = ?
                    AND dbo.Intermediario.AP_MAT = ?
                    AND dbo.Intermediario.ESTATUS = 1
                    """,
                    (nombre, apellido_paterno, apellido_materno),
                )
            # Verificar si el teléfono ya está en uso
            tel_existe = config.Read(
                    """
                    SELECT 
                        dbo.Intermediario.TEL
                    FROM dbo.Intermediario 
                    WHERE dbo.Intermediario.TEL = ?
                    """,
                    (int(telefono),),
                )
            # Cualquier error
            if existe or tel_existe:
                if existe:
                    ErrorIntermediarioRegistrado = True
                    raise MyException(
                            "ErrorIntermediary",
                            "The intermediary already exists in the DB.",
                        )
                if tel_existe:
                    ErrorIntermediarioTelefono = True
                    raise MyException(
                            "ErrorTel", "The phone number is already registered"
                        )
            if VerificarInactivo:
                CasoActualizarIntermediario = True
                config.CUD(
                        """
                        UPDATE dbo.Intermediario 
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
                config.CUD(
                        """
                        INSERT INTO dbo.Intermediario (NOMBRE, AP_PAT, AP_MAT, TEL, ESTATUS, ID_COMPANIA) 
                        VALUES (?, ?, ?, ?, 1, ?)
                        """,
                        (nombre, apellido_paterno, apellido_materno, int(telefono), int(company_id)),
                    )
                print("#################### FIN (Se inserto en la BD) ####################>")
        except MyException as ex:
            OtrosErroresCrearIntermediario = False
            Tipo, Mensaje = ex.args
            print(f"Type {Tipo} : {Mensaje}")
            flash(f"Type {Tipo} : {Mensaje}")
            print("#################### FIN (No se inserto) ####################>")
        except Exception as e:
            print(f"Type : {e}")
            flash(f"Type : {e}")
            print("#################### FIN (No se inserto) ####################>")
        return redirect(
            url_for(
                "products.manage_intermediary",
                ErrorIntermediarioTelefono=ErrorIntermediarioTelefono,
                ErrorIntermediarioRegistrado=ErrorIntermediarioRegistrado,
                OtrosErroresCrearIntermediario=OtrosErroresCrearIntermediario,
                CasoActualizarIntermediario=CasoActualizarIntermediario,
            )
        )


# Editar intermediario (Terminado)
@products.route("/edit_intermediary", methods=["GET", "POST"])
def edit_intermediary():
    # Errores
    ErrorIntermediarioTelefono = False
    ErrorIntermediarioRegistrado = False
    OtrosErroresEditarIntermediario = False
    print("<#################### edit_company ####################")
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
            # Verificar si el intermediario ya existe
            existe = config.Read(
                """
                SELECT 
                    dbo.Intermediario.NOMBRE,
                    dbo.Intermediario.AP_PAT,
                    dbo.Intermediario.AP_MAT
                FROM dbo.Intermediario 
                WHERE dbo.Intermediario.NOMBRE = ?
                AND dbo.Intermediario.AP_PAT = ?
                AND dbo.Intermediario.AP_MAT = ?
                AND dbo.Intermediario.ID_INTERMEDIARIO != ?
                """,
                (nombre, apellido_paterno, apellido_materno, int(id_intermediario)),
            )
            # Verificar si el teléfono ya está en uso
            tel_existe = config.Read(
                """
                SELECT 
                    dbo.Intermediario.TEL
                FROM dbo.Intermediario 
                WHERE dbo.Intermediario.TEL = ?
                """,
                (telefono,),
            )
            # Cualquier error
            if existe or tel_existe:
                if existe:
                    raise MyException(
                        "ErrorIntermediary",
                        "The intermediary already exists in the DB.",
                    )
                if tel_existe:
                    raise MyException(
                        "ErrorTel", "The phone number is already registered"
                    )
            else:
                # Actualizar en la base de datos
                config.CUD(
                    """
                    UPDATE dbo.Intermediario 
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
                print("#################### FIN ####################>")
        except MyException as ex:
            Tipo, Mensaje = ex.args
            print(f"Type {Tipo} : {Mensaje}")
            flash(f"Type {Tipo} : {Mensaje}")
            print("#################### FIN (No se inserto) ####################>")
        except Exception as e:
            OtrosErroresEditarIntermediario = True
            print(f"Type : {e}")
            flash(f"Type : {e}")
            print("#################### FIN (No se inserto) ####################>")
        return redirect(
            url_for(
                "products.manage_intermediary",
                ErrorIntermediarioTelefono=ErrorIntermediarioTelefono,
                ErrorIntermediarioRegistrado=ErrorIntermediarioRegistrado,
                OtrosErroresEditarIntermediario=OtrosErroresEditarIntermediario,
            )
        )


# Agregar Ventas
@sales.route("/addsalesworker")
def addsalesworker():
    # Errores
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    products = config.Read(
                """
                SELECT 
                    ID_PRODUCTO, 
                    NOMBRE, 
                    PRECIO_UNITARIO, 
                    EXISTENCIAS,
                    ESTATUS
                FROM dbo.Almacen 
                WHERE dbo.Almacen.ESTATUS = 1
                """
            )
    print(
        "#################### FIN (sales/add-sales-worker.html) ####################>"
    )
    return render_template(
        "sales/add-sales-worker.html", 
        products=products, 
        IsAdmin=session["ES_ADMIN"]
    )

# Realizar Venta
@sales.route("/MakeSales", methods=["POST"])
def MakeSales():
    # Errores
    ErrorCantidad = False
    ErrorPrecio = False
    ErrorProductoInexistente = False
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    # Capa 2:
    if request.method == "POST":
        try:
            print("<#################### MakeSales ####################")
            sales_data = request.get_json()
            Entrada = []
            print("Sales Data Received:", sales_data)
            for i in range(len(sales_data)):
                id = sales_data[i].get("id")
                cantidad = sales_data[i].get("quantity")
                print("ID>",id) # El id
                print("cantidad>",cantidad)
                Entrada.append([int(id), int(cantidad)])
            #
            print("<==================== DATOS OBTENIDOS ====================")
            for producto in Entrada:
                print(producto)
            print("========================================>")
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
                    ExisteProducto
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
                    """
                    SELECT dbo.Mes.ID_MES 
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
                        SumaIva += IvaValue  # Sumar los iva por producto
                        TotalProductos += Entrada[i][
                            1
                        ]  # Sumar la cantidad de productos
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
                    #
                    config.CUD(
                        """
                        INSERT INTO dbo.Ventas (CANTIDAD_VENTA, TOTAL, ESTATUS, ID_DIA, ID_MES, ID_ANIO) 
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
                    id = int(
                        config.Read("SELECT IDENT_CURRENT('dbo.Ventas') AS NewID")[
                            0
                        ][0]
                    )
                    #
                    print("ID-VENTA>", id)
                    for y in range(len(TablaDetalles)):
                        config.CUD(
                            """
                            INSERT INTO dbo.Detalles(CANTIDAD,IMPORTE,IVA,ESTATUS,ID_PRODUCTO,ID_VENTA) 
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
                            UPDATE dbo.Almacen 
                            SET 
                                EXISTENCIAS = ?, 
                                PRECIO_EXISTENCIA = ?,
                                ESTATUS = ?
                            WHERE ID_PRODUCTO = ?
                            """,
                            (
                                int(tabla[z][2] - Entrada[z][1]),
                                int(tabla[i][1]*(tabla[z][2] - Entrada[z][1])),
                                ESTATUS,
                                int(tabla[z][0]),
                            ),
                        )
                return redirect(url_for("sales.addsalesworker"))
            else:
                print("No existe producto")
        except Exception as e:
            print(e)
    print("#################### FIN  ####################>")
    return redirect(url_for("sales.addsalesworker"))


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
            SELECT dbo.Detalles.ID_PRODUCTO, dbo.Almacen.NOMBRE, dbo.Detalles.CANTIDAD, dbo.Detalles.IMPORTE, dbo.Detalles.IVA
            FROM dbo.Almacen, dbo.Detalles
            WHERE dbo.Almacen.ID_PRODUCTO = dbo.Detalles.ID_PRODUCTO
            AND dbo.Detalles.ID_VENTA = ?
            """,
            (sale_id,),
        )
        sales = config.Read(
            """
            SELECT 
                dbo.Ventas.ID_VENTA, 
                dbo.Dia.DIA, 
                dbo.Mes.MES, 
                dbo.Anio.ANIO, 
                dbo.Ventas.CANTIDAD_VENTA, 
                dbo.Ventas.TOTAL
            FROM dbo.Ventas, dbo.Dia, dbo.Mes, dbo.Anio
            WHERE dbo.Ventas.ID_DIA = dbo.Dia.ID_DIA
            AND dbo.Ventas.ID_MES = dbo.Mes.ID_MES
            AND dbo.Ventas.ID_ANIO = dbo.Anio.ID_ANIO
            """
        )
        return render_template("sales/report-sales.html", sales=sales, details=details,IsAdmin=session["ES_ADMIN"])

    # Capa 4: Obtener todas las ventas si no hay método POST
    print("<==================== DATOS OBTENIDOS ====================")
    sales = config.Read(
        """
        SELECT 
            dbo.Ventas.ID_VENTA, 
            dbo.Dia.DIA, 
            dbo.Mes.MES, 
            dbo.Anio.ANIO, 
            dbo.Ventas.CANTIDAD_VENTA, 
            dbo.Ventas.TOTAL
        FROM dbo.Ventas, dbo.Dia, dbo.Mes, dbo.Anio
        WHERE dbo.Ventas.ID_DIA = dbo.Dia.ID_DIA
        AND dbo.Ventas.ID_MES = dbo.Mes.ID_MES
        AND dbo.Ventas.ID_ANIO = dbo.Anio.ID_ANIO
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


# Ruta dinámica para archivos estáticos
@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(debug=True)

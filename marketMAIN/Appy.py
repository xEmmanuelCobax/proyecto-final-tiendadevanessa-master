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

import config, locale, re # Importar config.py en donde se hacen las consultas de la base de datos
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


# Bienvenida (Terminado)
@p.route("/welcomeuser") 
def welcomeuser():
    # Errores
    if "email" in session:
        print("<#################### welcomeuser ####################")
        print("Session > ",session)
        print("Nombre > ",session['name'])
        print("Es admin? > ", session["ES_ADMIN"])
        print("#################### FIN ####################>")
        return render_template(
            "profile/welcome-user.html",
            user=session["name"],
            IsAdmin=session["ES_ADMIN"],
        )
    else:
        print("#################### NO HAY SESSION ####################>")
        return redirect(
            url_for("auth.signin")
        )

# Iniciar session (Terminado)
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    # Errores
    email_not_found = True  # El correo electrónico no está registrado
    bad_password = True  # Contraseña incorrecta
    print("<#################### RUTA-Signing ####################")
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
            return redirect(url_for("auth.signin"))
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
        )
    print("#################### Return to auth/signin.html ####################>")
    return render_template("auth/signin.html")


# Registrarse (Terminado)
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # Errores
    email_found = False # El email ya esta registrado
    user_found = False  #   El usuario ya ha sido encontrado
    # Otros booleanos
    registration_successful = False
    print("<#################### RUTA-Signup ####################")
    # Verificar si hay una dirección de correo dentro de la sesión
    if "email" in session:
        print("#################### Session iniciada renderizar index.html ####################>")
        return render_template("index.html", email=session["email"])
    elif request.method == "POST":
        # Obtener datos del formulario
        name = request.form.get("name")
        apellido_paterno = request.form.get("paternal_lastname")
        apellido_materno = request.form.get("maternal_lastname")
        email = request.form.get("email")
        password = request.form.get("password")
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
            return render_template(
                "auth/signup.html",
                registration_successful=registration_successful,
                user=user,
            )
    else:
        print("#################### Renderizar auth/signup.html ####################>")
        return render_template("auth/signup.html")


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
    if "email" in session and session["ES_ADMIN"]:
        # Renderizar con los datos
        return render_template(
            "products/warehouse.html",
            products=ConsultaPIA(),
            IsAdmin=session["ES_ADMIN"],
        )
    else:
        return redirect(url_for("auth.signin"))


# Manejar el inventario (Terminado)
@products.route("/manage_warehouse", methods=["GET", "POST"])
def managewarehouse():
    if "email" in session and session["ES_ADMIN"]:
        # Errores
        OtrosErroresBorrarProducto = request.args.get('OtrosErroresBorrarProducto')
        OtrosErroresCrearProducto = request.args.get('OtrosErroresCrearProducto')
        OtrosErroresActualizarProducto = request.args.get(
            'OtrosErroresActualizarProducto'
        )
        ErrorCantidad = request.args.get(
            'ErrorCantidad'
        )
        ErrorPrecio = request.args.get(
            'ErrorPrecio'
        )
        ErrorProductoExiste = request.args.get(
            'ErrorProductoExiste'
        )
        ErrorRelacion = request.args.get(
            'ErrorRelacion'
        )
        CasoActivarProducto = request.args.get(
            'CasoActivarProducto'
        )
        # Renderizar con los datos
        print("OtrosErroresBorrarProducto > ",OtrosErroresBorrarProducto)
        print("OtrosErroresCrearProducto > ",OtrosErroresCrearProducto)
        print("OtrosErroresActualizarProducto > ", OtrosErroresActualizarProducto)
        #
        print("ErrorCantidad > ", ErrorCantidad)
        print("ErrorPrecio > ", ErrorPrecio)
        print("ErrorProductoExiste > ", ErrorProductoExiste)
        print("ErrorRelacion > ", ErrorRelacion)
        print("ErrorRelacion > ", CasoActivarProducto)
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
        )
    else:
        return redirect(url_for("auth.signin"))


# Buscar producto (Terminado)
@products.route("/search_product", methods=["GET", "POST"])
def search_product():
    products = []
    if "email" in session and session["ES_ADMIN"]:
        if request.method == "POST":
            print("<#################### BUSCAR PRODUCTOS ####################")
            search_term = (str(request.form.get("search_term"))).strip()
            # Pruebas
            print("<==================== DATOS OBTENIDOS ====================")
            print(f"nombre - {search_term}")
            print("========================================>")
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
            print("#################### FIN ####################>")
        return render_template("products/warehouse.html", products=products)
    else:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("auth.signin"))


# Borrar producto (Terminado)
@products.route("/delete_product", methods=["POST"])
def delete_product():
    # Errores
    OtrosErroresBorrarProducto=False
    # Verificar si el usuario tiene una sesión activa
    if "email" in session and session["ES_ADMIN"]:
        # Verificar si el método de solicitud es POST
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
    else:
        # Si el usuario no tiene una sesión activa, redirigirlo a la página de inicio de sesión
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("auth.signin"))


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
    if "email" in session and session["ES_ADMIN"]:
        print("<#################### CREAR PRODUCTOS ####################")
        if request.method == "POST":
            try:
                # Obtener datos del formulario
                marca = (request.form.get("marca"))
                producto = (request.form.get("producto"))
                # Unidad de medida
                unit_quantity = int(request.form.get("unitquantity")  )# Cantidad
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
    else:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("auth.signin"))


# Actualizar producto (En desarrollo*)
@products.route("/update_product", methods=["POST"])
def update_product() :
    # Errores
    ErrorCantidad = False
    ErrorPrecio = False
    ErrorProductoExiste = False
    ErrorRelacion = False
    OtrosErroresActualizarProducto = False
    if "email" in session and session["ES_ADMIN"]:
        print("<#################### Actualizar PRODUCTOS ####################")
        if request.method == "POST":
            try:
                # Obtener datos del formulario
                product_id = int(request.form.get("editproduct_id"))
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
                    quantity = str(unit_quantity)+ "custom"
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
                    (int(intermediario), int(compania),),
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
    else:    
        print("#################### NO HAY SESSION ####################>")
        return redirect(
            url_for("auth.signin"),
        )


# Manejar los intermediario (En Desarrollo)
@products.route("/manage_company")
def managecompany():
    # Errores
    OtrosErroresBorrarIntermediario=request.args.get('OtrosErroresBorrarIntermediario')
    OtrosErroresCrearIntermediario=request.args.get('OtrosErroresCrearIntermediario')
    OtrosErroresEditarIntermediario=request.args.get('OtrosErroresEditarIntermediario')
    ErrorIntermediarioTelefono=request.args.get('ErrorIntermediarioTelefono')
    ErrorIntermediarioRegistrado=request.args.get('ErrorIntermediarioRegistrado')
    # Casos
    CasoActualizarIntermediario = request.args.get("CasoActualizarIntermediario")
    if "email" in session and session["ES_ADMIN"]:
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
        return render_template("products/manage-company.html", relations=relations, 
                            companies=ConsultaCompanias(),
                            OtrosErroresBorrarIntermediario=OtrosErroresBorrarIntermediario,
                            OtrosErroresCrearIntermediario=OtrosErroresCrearIntermediario,
                            OtrosErroresEditarIntermediario=OtrosErroresEditarIntermediario,
                            ErrorIntermediarioTelefono=ErrorIntermediarioTelefono,
                            ErrorIntermediarioRegistrado=ErrorIntermediarioRegistrado,
                            CasoActualizarIntermediario=CasoActualizarIntermediario,
                            )
    else:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("auth.signin"))


# Borrar intermediarios (En Desarrollo)
@products.route("/delete_company", methods=["POST"])
def delete_company():
    # Errores
    OtrosErroresBorrarIntermediario = False
    # Verificar si el usuario tiene una sesión activa
    if "email" in session and session["ES_ADMIN"]:
        # Verificar si el método de solicitud es POST
        if request.method == "POST":
            try:
                print("<#################### delete_company ####################")
                # Obtener el ID del intermediario de los datos del formulario
                id_intermediario = int(request.form.get("DeleteIntermediaryId")) #Se obtiene de un dato oculto
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
            except Exception as ex:
                print("Hola papus")
            return redirect(url_for("products.managecompany"))
    # Si el usuario no tiene una sesión activa, redirigirlo a la página de inicio de sesión
    else:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("auth.signin"))


# crear intermediario (En Desarrollo)
@products.route("/create_company", methods=["POST"])
def create_company():
    # Errores
    ErrorIntermediarioTelefono = False
    ErrorIntermediarioRegistrado = False
    OtrosErroresCrearIntermediario = False
    CasoActualizarIntermediario = False
    if "email" in session and session["ES_ADMIN"]:
        print("<#################### CREAR EMPRESA ####################")
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
                    "products.managecompany",
                    ErrorIntermediarioTelefono=ErrorIntermediarioTelefono,
                    ErrorIntermediarioRegistrado=ErrorIntermediarioRegistrado,
                    OtrosErroresCrearIntermediario=OtrosErroresCrearIntermediario,
                    CasoActualizarIntermediario=CasoActualizarIntermediario
                )
            )
    else:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("auth.signin"))


# Editar intermediario (En Desarrollo)
@products.route("/edit_company", methods=["GET", "POST"])
def edit_company():
    # Errores
    ErrorIntermediarioTelefono = False
    ErrorIntermediarioRegistrado = False
    OtrosErroresEditarIntermediario = False
    if "email" in session and session["ES_ADMIN"]:
        print("<#################### EDITAR EMPRESA ####################")
        # Verificar si el método es POST para procesar el formulario
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
                    "products.managecompany",
                    ErrorIntermediarioTelefono=ErrorIntermediarioTelefono,
                    ErrorIntermediarioRegistrado=ErrorIntermediarioRegistrado,
                    OtrosErroresEditarIntermediario=OtrosErroresEditarIntermediario,
                )
            )
    else:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("auth.signin"))

# Ajuste de perfil (En Desarrollo)
@p.route("/profile")
def profile():
    return render_template("profile/profile.html")


# Ni idea
@sc.route("/shortcut")
def shortcut():
    return render_template("shortcut.html")


# Ni idea
@sc.route("/settings")
def settings():
    return render_template("settings/settings.html")


# Ventas
@sales.route("/addsalesworker")
def addsalesworker():
    # Errores 

    # sales.addsalesworker
    if "email" in session:
        print("<#################### addsalesworker ####################")
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
        print("#################### FIN en addsalesworker ####################>")
        return render_template("sales/add-sales-worker.html", products=products)
    else:
        print("#################### NO HAY SESSION ####################>")
    return redirect(url_for("auth.signin"))


@sales.route("/MakeSales", methods=["POST"])
def MakeSales():
    if "email" in session:
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
    else:
        print("NO HAY SESSION")
    return redirect(url_for("auth.signin"))

# Cerrar session (Terminado)
@app.route("/signout")
def signout():
    if "email" in session:
        print("<#################### CERRANDO SESSION... ####################")
        session.pop("email", None)
        print("#################### FIN ####################>")
        return redirect(url_for("auth.signin"))
    else:
        print("NO HAY SESSION")
    return redirect(url_for("auth.signin"))


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


# Ruta Principal
@app.route("/")
def index():
    if "email" in session:
        return redirect(url_for("shortcut.shortcut"))
    else: 
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

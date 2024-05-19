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
)
import config  # Importar config.py en donde se hacen las consultas de la base de datos

app = Flask(__name__)

auth = Blueprint("auth", __name__, url_prefix="/auth")
products = Blueprint("products", __name__, url_prefix="/products")
p = Blueprint("profile", __name__, url_prefix="/profile")
sc = Blueprint("shortcut", __name__, url_prefix="/shortcut")

app.config["SECRET_KEY"] = config.HEX_SEC_KEY


# Iniciar session (Terminado)
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    print("========================================\nRUTA-Signing\n")
    if "email" in session:
        print("========================================\nEmail In Session\n")
        return render_template("profile/welcome-user.html", email=session["email"])
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print("========================================\nDATOS OBTENIDOS>\n")
        print(f"Email - {email}")
        print(f"Password - {password}")
        print("========================================")
        existing_email = config.Read(
            "SELECT * FROM dbo.Usuarios WHERE CORREO = '{}'".format(email)
        )

        if not existing_email:
            # El correo electrónico no está registrado
            email_not_found = True
            print(
                "========================================\nCorreo electrónico no está registrado\n========================================"
            )
            return render_template("auth/signin.html", email_not_found=email_not_found)

        else:
            # El correo electrónico está registrado
            if existing_email[0][6] == password:
                # Contraseña correcta
                session["email"] = email
                print(
                    "========================================\nContraseña correcta\n========================================"
                )
                return redirect(url_for("profile.welcomeuser", user=email))
            else:
                # Contraseña incorrecta
                bad_password = True
                print(
                    "========================================\nContraseña incorrecta\n========================================"
                )
                return render_template(
                    "auth/signin.html", bad_password=bad_password, email=email
                )
    print("========================================\nReturn to auth/signin.html\n")
    return render_template("auth/signin.html")


# Registrarse (Terminado)
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    print("<#################### RUTA-Signup ####################")
    # Verificar si hay una dirección de correo dentro de la sesión
    if "email" in session:
        print("#################### Session iniciada renderizar index.html ####################>")
        return render_template("index.html", email=session["email"])
    elif request.method == "POST":
        # Manejo de errores
        email_found = False
        user_found = False
        lastname_error = False
        # Obtener datos del formulario
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        # Prubas
        print("<==================== DATOS OBTENIDOS ====================")
        print(f"Name - {name}")
        print(f"Lastname - {lastname}")
        print(f"Email - {email}")
        print(f"Password - {password}")
        print("========================================>")
        # Obtener desde el lastname los dos apellidos
        aux = lastname.split()
        # Si el len del auxiliar entonces tiene dos apellidos, por lo que entra.
        if len(aux) == 2:
            apellido_paterno = aux[0]  # El primer elemento es el apellido paterno
            apellido_materno = aux[-1]  # El último elemento es el apellido materno
        else:
            # Error en el apellido
            lastname_error = True
        # Consulta para verificar si existe el correo en la BD
        existing_email = config.Read(
            "SELECT * FROM dbo.Usuarios WHERE CORREO = '{}'".format(email)
        )
        # Consulta para verificar si existe el usuario en la BD
        existing_user = config.Read(
            "SELECT * FROM dbo.Usuarios WHERE NOMBRE = '{}' AND AP_PAT = '{}' AND AP_MAT = '{}'".format(
                name, apellido_paterno, apellido_materno
            )
        )
        # Existe el correo en la base de datos
        if existing_email:
            email_found = True
        # Existe el usuario en la base de datos
        if existing_user:
            user_found = True
        # Cualquier error
        if existing_email or existing_user or lastname_error:
            return render_template(
                "auth/signup.html",
                user_found=user_found,
                email_found=email_found,
                lastname_error=lastname_error,
            )
        # No hay ningún error
        else:
            # Registrar en base de datos
            config.CUD(
                "INSERT INTO dbo.Usuarios (NOMBRE, AP_PAT, AP_MAT, CORREO, CONTRASENA, ESTATUS) VALUES (?, ?, ?, ?, ?, 1)",
                (name, apellido_paterno, apellido_materno, email, password),
            )
            print("#################### Renderizar auth/signin ####################>")
            return redirect(url_for("auth.signin", registration_successful=True))
    else:
        print("#################### Renderizar auth/signup.html ####################>")
        return render_template("auth/signup.html")


# Registro exitoso (Terminado)
@app.route("/successful_registration")
def successful_registration():
    return render_template("auth/successful-registration.html")


# Crear producto (En Prueba)
@products.route("/create_product", methods=["POST"])
def create_product():
    if "email" in session:
        print("<#################### CREAR PRODUCTOS ####################")
        if request.method == "POST":
            # Obtener datos del formulario
            marca = request.form.get("marca")
            producto = request.form.get("producto")
            # Unidad de medida
            unit_quantity = request.form.get("unitquantity")  # Cantidad
            seslect_unit_quantity = request.form.get(
                "SelectUnitOfMeasure"
            )  # Unidad de medida
            # Piezas
            if seslect_unit_quantity == "pieces":
                quantity = unit_quantity + "Pzs"
            # Litros
            elif seslect_unit_quantity == "liters":
                quantity = unit_quantity + "l"
            # Milimetros
            elif seslect_unit_quantity == "milliliters":
                quantity = unit_quantity + "ml"
            # Kilogramos
            elif seslect_unit_quantity == "kilogram":
                quantity = unit_quantity + "kg"
            # Gramos
            elif seslect_unit_quantity == "grams":
                quantity = unit_quantity + "gr"
            # custom?
            else:
                quantity = unit_quantity + "No se"
            # Datos formados
            nombre = f"{marca}_{producto}_{quantity}"
            cantidad = request.form.get("cantidad")
            precio = request.form.get("precio")
            compania = request.form.get("company_id")
            intermediario = request.form.get("intermedary_id")
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
                "SELECT ID_INTERMEDIARIO, Intermediario.NOMBRE, Intermediario.AP_PAT, Intermediario.AP_MAT, Proveedor.ID_COMPANIA, Proveedor.NOMBRE "
                "FROM dbo.Proveedor "
                "INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA "
                "WHERE dbo.Proveedor.ESTATUS = 1 AND dbo.Intermediario.ESTATUS = 1 AND dbo.Intermediario.ID_INTERMEDIARIO = {} AND dbo.Proveedor.ID_COMPANIA = {}".format(
                    intermediario, compania
                )
            )
            print("========================================>")
            # Verificar si el producto ya existe
            print(
                "<==================== VERIFICAR SI EL PRODUCTO EXISTE ===================="
            )
            productoexiste = config.Read(
                "SELECT dbo.Almacen.NOMBRE FROM dbo.Almacen WHERE dbo.Almacen.NOMBRE = '{}'".format(
                    nombre
                )
            )
            print("========================================>")
            # Condiciones
            print("<==================== ACCIONES ====================")
            if productoexiste:
                # Si el producto ya existe, redireccionar con un mensaje de error
                print(
                    "====================! Producto existente en la BD.====================>"
                )
                print("#################### FIN ####################>")
                return redirect(url_for("products.warehouse"))
            elif existe:
                # Insertar el nuevo producto en la base de datos   
                config.CUD(
                    "INSERT INTO dbo.Almacen (NOMBRE, PRECIO_UNITARIO, EXISTENCIAS, PRECIO_EXISTENCIA, ID_INTERMEDIARIO, ESTATUS) "
                    "VALUES (?, ?, ?, ?, ?, 1)",
                    (nombre, precio, cantidad, float(precio) * int(cantidad), intermediario)
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
                print("#################### FIN ####################>")
            return redirect(url_for("products.warehouse"))
    else:
        return redirect(url_for("auth.signin"))


# Actualizar producto (En desarrollo*)
@products.route("/update_product", methods=["POST"])
def update_product():
    if "email" in session:
        print("<#################### Actualizar PRODUCTOS ####################")
        if request.method == "POST":
            # Obtener datos del formulario
            product_id = request.form.get("editproduct_id")
            marca = request.form.get("newmarca")
            producto = request.form.get("newproducto")
            # Unidad de medida
            unit_quantity = request.form.get("editunitquantity")  # Cantidad
            seslect_unit_quantity = request.form.get(
                "EditSelectUnitOfMeasure"
            )  # Unidad de medida
            # Piezas
            if seslect_unit_quantity == "pieces":
                quantity = unit_quantity + "Pzs"
            # Litros
            elif seslect_unit_quantity == "liters":
                quantity = unit_quantity + "l"
            # Milimetros
            elif seslect_unit_quantity == "milliliters":
                quantity = unit_quantity + "ml"
            # Kilogramos
            elif seslect_unit_quantity == "kilogram":
                quantity = unit_quantity + "kg"
            # Gramos
            elif seslect_unit_quantity == "grams":
                quantity = unit_quantity + "gr"
            # custom?
            else:
                quantity = unit_quantity + "No se"
            # Datos formados
            nombre = f"{marca}_{producto}_{quantity}"
            cantidad = request.form.get("newcantidad")
            precio = request.form.get("newprecio")
            compania = request.form.get("company-new-select")
            intermediario = request.form.get("intermedary-new-select")
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
                "SELECT ID_INTERMEDIARIO, Intermediario.NOMBRE, Intermediario.AP_PAT, Intermediario.AP_MAT, Proveedor.ID_COMPANIA, Proveedor.NOMBRE "
                "FROM dbo.Proveedor "
                "INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA "
                "WHERE dbo.Proveedor.ESTATUS = 1 AND dbo.Intermediario.ESTATUS = 1 AND dbo.Intermediario.ID_INTERMEDIARIO = {} AND dbo.Proveedor.ID_COMPANIA = {}".format(
                    intermediario, compania
                )
            )
            print("========================================>")
            # Verificar si el producto ya existe
            print(
                "<==================== VERIFICAR SI EL PRODUCTO EXISTE ===================="
            )
            productoexiste = config.Read(
                "SELECT dbo.Almacen.NOMBRE FROM dbo.Almacen WHERE dbo.Almacen.NOMBRE = '{}'".format(
                    nombre
                )
            )
            print("========================================>")
            # Condiciones
            print("<==================== ACCIONES ====================")
            if productoexiste:
                # Si el producto ya existe con un nombre diferente, redireccionar con un mensaje de error
                print(
                    "====================! Producto existente en la BD.====================>"
                )
                flash(
                    "El producto ya existe en la base de datos con un nombre diferente."
                )
                return redirect(url_for("products.warehouse"))
            elif not existe:
                # Si la compañía o el intermediario no cumplen las condiciones, redireccionar con un mensaje de error
                print(
                    "====================! La compañía o el intermediario no cumplen las condiciones necesarias.====================>"
                )
                flash(
                    "La compañía o el intermediario no cumplen las condiciones necesarias."
                )
                return redirect(url_for("products.warehouse"))
            else:
                # Actualizar el producto en la base de datos
                config.CUD(
                    "UPDATE dbo.Almacen SET NOMBRE = ?, PRECIO_UNITARIO = ?, EXISTENCIAS = ?, PRECIO_EXISTENCIA = ?, ID_INTERMEDIARIO = ?, ESTATUS = 1 WHERE ID_PRODUCTO = ?",
                    (
                        nombre,
                        precio,
                        cantidad,
                        float(precio) * int(cantidad),
                        intermediario,
                        product_id,
                    ),
                )
                print(
                    "====================! Producto actualizado exitosamente. !====================>"
                )
                flash("Producto actualizado exitosamente.")
                return redirect(url_for("products.warehouse"))
    else:
        return redirect(url_for("auth.signin"))


# Mostrar los productos (Terminado)
@products.route("/warehouse")
def warehouse():
    if "email" in session:
        products = config.Read(
            "SELECT ID_PRODUCTO, NOMBRE, PRECIO_UNITARIO, EXISTENCIAS FROM dbo.Almacen WHERE dbo.Almacen.ESTATUS = 1"
        )
        return render_template("products/warehouse.html", products=products)
    else:
        return redirect(url_for("auth.signin"))


# Borrar producto (Terminado)
@products.route("/delete_product", methods=["POST"])
def delete_product():
    # Verificar si el usuario tiene una sesión activa
    if "email" in session:
        # Verificar si el método de solicitud es POST
        if request.method == "POST":
            # Obtener el ID del producto de los datos del formulario
            product_id = request.form.get("product_id")
            print("<==================== DATOS OBTENIDOS ====================")
            print(f"Product_ID - {product_id}")
            print("========================================>")
            config.CUD(
                "UPDATE dbo.Almacen SET ESTATUS = 0 WHERE ID_PRODUCTO = ?",
                (product_id,)
            )
            print("#################### FIN ####################>")
            return redirect(url_for("products.managewarehouse"))
    # Si el usuario no tiene una sesión activa, redirigirlo a la página de inicio de sesión
    return redirect(url_for("auth.signin"))


# Buscar producto (Terminado)
@products.route("/search_product", methods=["GET", "POST"])
def search_product():
    products = []
    if "email" in session:
        if request.method == "POST":
            print("<#################### BUSCAR PRODUCTOS ####################")
            search_term = request.form.get("search_term")
            # Pruebas
            print("<==================== DATOS OBTENIDOS ====================")
            print(f"nombre - {search_term}")
            print("========================================>")
            query = "SELECT dbo.Almacen.ID_PRODUCTO ,dbo.Almacen.NOMBRE, dbo.Almacen.PRECIO_UNITARIO, dbo.Almacen.EXISTENCIAS FROM  dbo.Almacen WHERE NOMBRE LIKE'%{}%' and dbo.Almacen.ESTATUS = 1;".format(
                search_term
            )
            products = config.Read(query)
            print("#################### FIN ####################>")
        return render_template("products/warehouse.html", products=products)
    else:
        print("#################### FIN ####################>")
        return redirect(url_for("auth.signin"))


# Manejar el inventario (Terminado)
@products.route("/manage_warehouse", methods=["GET", "POST"])
def managewarehouse():
    if "email" in session:
        companies = []
        relations = []
        print("<#################### manage_warehouse ####################")
        # Consulta para mostrar los productos
        products = config.Read(
            "SELECT ID_PRODUCTO, NOMBRE, PRECIO_UNITARIO, EXISTENCIAS FROM dbo.Almacen WHERE dbo.Almacen.ESTATUS = 1"
        )
        # Consulta para mostrar compania
        companies = config.Read(
            "SELECT DISTINCT dbo.Proveedor.ID_COMPANIA, dbo.Proveedor.NOMBRE  FROM dbo.Proveedor  INNER JOIN dbo.Intermediario ON dbo.Intermediario.ID_COMPANIA = dbo.Proveedor.ID_COMPANIA WHERE dbo.Proveedor.ESTATUS = 1 AND dbo.Intermediario.ESTATUS = 1;SELECT * FROM dbo.Intermediario WHERE dbo.Intermediario.ESTATUS = 1;"
        )
        # Consulta para poder relaciones entre compania - intermediario
        relations = config.Read(
            "SELECT dbo.Proveedor.ID_COMPANIA,dbo.Proveedor.NOMBRE,dbo.Intermediario.ID_INTERMEDIARIO,dbo.Intermediario.NOMBRE, dbo.Intermediario.AP_PAT, dbo.Intermediario.AP_MAT FROM dbo.Proveedor INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA WHERE dbo.Proveedor.ESTATUS = 1 AND dbo.Intermediario.ESTATUS = 1;"
        )
        # Renderizar con los datos
        print("#################### FIN ####################>")
        return render_template(
            "products/manage-warehouse.html",
            products=products,
            relations=relations,
            companies=companies,
        )
    else:
        return redirect(url_for("auth.signin"))


# Manejar la companias (En Planteamiento)
@products.route("/manage_company")
def managecompany():
    if "email" in session:
        companies = []
        relations = []
        relations = config.Read(
            "SELECT dbo.Proveedor.ID_COMPANIA ,dbo.Proveedor.NOMBRE, dbo.Intermediario.ID_INTERMEDIARIO, Intermediario.NOMBRE, Intermediario.AP_PAT, Intermediario.AP_MAT, dbo.Intermediario.TEL FROM dbo.Proveedor INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA WHERE dbo.Proveedor.ESTATUS = 1 AND dbo.Intermediario.ESTATUS = 1"
        )
        companies = config.Read(
            "SELECT DISTINCT dbo.Proveedor.ID_COMPANIA, dbo.Proveedor.NOMBRE  FROM dbo.Proveedor  INNER JOIN dbo.Intermediario ON dbo.Intermediario.ID_COMPANIA = dbo.Proveedor.ID_COMPANIA WHERE dbo.Proveedor.ESTATUS = 1 AND dbo.Intermediario.ESTATUS = 1;SELECT * FROM dbo.Intermediario WHERE dbo.Intermediario.ESTATUS = 1;"
        )
        return render_template("products/manage-company.html", relations=relations, companies=companies)
    else:
        return redirect(url_for("auth.signin"))


# Borrar companias (En Planteamiento)
@products.route("/delete_company", methods=["POST"])
def delete_company():
    # Verificar si el usuario tiene una sesión activa
    if "email" in session:
        # Verificar si el método de solicitud es POST
        if request.method == "POST":
            print("<#################### delete_company ####################")
            # Obtener el ID del intermediario de los datos del formulario
            company_id = request.form.get("company_id")
            print("<==================== DATOS OBTENIDOS ====================")
            print(f"company_id - {company_id}")
            print("========================================>")
            config.CUD(
                """
                UPDATE dbo.Intermediario SET ESTATUS = 0 WHERE ID_COMPANIA = ?;
                UPDATE dbo.Proveedor SET ESTATUS = 0 WHERE ID_COMPANIA = ?;
                """,
                (company_id, company_id)
            )
            print("#################### FIN ####################>")
            return redirect(url_for("products.managecompany"))
    # Si el usuario no tiene una sesión activa, redirigirlo a la página de inicio de sesión
    return redirect(url_for("auth.signin"))


# crear conpañia (En Planteamiento)
@products.route("/create_company", methods=["POST"])
def create_company():
    if "email" in session:
        print("<#################### CREAR EMPRESA ####################")
        if request.method == "POST":
            # Errores
            lastname_error = False
            # Obtener datos del formulario
            nombre = request.form.get("intermediaryName")
            apellidos = request.form.get("intermediaryLastName")
            telefono = request.form.get("intermediaryPhone")
            company_id = request.form.get("company_id")
            # Obtener desde el lastname los dos apellidos
            aux = apellidos.split()
            # Si el len del auxiliar entonces tiene dos apellidos, por lo que entra.
            if len(aux) == 2:
                apellido_paterno = aux[0]  # El primer elemento es el apellido paterno
                apellido_materno = aux[-1]  # El último elemento es el apellido materno
            else:
                # Error en el apellido
                lastname_error = True
            # Pruebas
            print("<==================== DATOS OBTENIDOS ====================")
            print(f"nombre - {nombre}")
            print(f"AP_MAT - {apellido_paterno}")
            print(f"AP_MAT - {apellido_materno}")
            print(f"TEL - {telefono}")
            print(f"company_id - {company_id}")
            print("========================================>")
            # Cualquier error
            if lastname_error:
                print("#################### FIN ####################>")
                return render_template(
                    "Manage-warehouse.html",
                    lastname_error=lastname_error,
                )
            else:
                # Insertar en la base de datos
                config.CUD(
                    "INSERT INTO dbo.Intermediario (NOMBRE,AP_PAT,AP_MAT,TEL,ESTATUS,ID_COMPANIA) VALUES (?,?,?,?,1,?)",
                    (
                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        telefono,
                        company_id
                    )
                )
                print("#################### FIN ####################>")
            return redirect(url_for("products.managecompany"))
    else:
        return redirect(url_for("auth.signin"))


# Bienvenida (Terminado)
@p.route("/welcomeuser") 
def welcomeuser():
    if "email" in session:
        print("<#################### welcomeuser ####################")
        print(session)
        print("#################### FIN ####################>")
        return render_template("profile/welcome-user.html")
    else:
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

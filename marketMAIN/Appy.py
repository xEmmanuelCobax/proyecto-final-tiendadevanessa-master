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


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    print("========================================\nRUTA-Signup\n")
    # Verificar si hay una dirección de correo dentro de la sesión
    if "email" in session:
        return render_template("index.html", email=session["email"])
    elif request.method == "POST":
        email_found = False
        user_found = False
        lastname_error = False

        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        print("========================================\nDATOS OBTENIDOS>\n")
        print(f"Name - {name}")
        print(f"Lastname - {lastname}")
        print(f"Email - {email}")
        print(f"Password - {password}")
        print("========================================")

        aux = lastname.split()
        if len(aux) >= 2:
            apellido_paterno = aux[0]  # El primer elemento es el apellido paterno
            apellido_materno = aux[-1]  # El último elemento es el apellido materno
        else:
            lastname_error = True

        existing_email = config.Read(
            "SELECT * FROM dbo.Usuarios WHERE CORREO = '{}'".format(email)
        )

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
                "INSERT INTO dbo.Usuarios (NOMBRE, AP_PAT , AP_MAT , CORREO , CONTRASENA, ESTATUS) VALUES ('{}', '{}', '{}', '{}', '{}' , 1)".format(
                    name, apellido_paterno, apellido_materno, email, password
                )
            )
            print("Renderizar auth/signin")
            return redirect(url_for("auth.signin", registration_successful=True))
    else:
        return render_template("auth/signup.html")


@app.route("/successful_registration")
def successful_registration():
    return render_template("auth/successful-registration.html")


@products.route("/create_product", methods=["POST"])
def create_product():
    if "email" in session:
        if request.method == "POST":
            # En la tabla Almacen
            nombre = request.form.get("nombre")
            cantidad = request.form.get("cantidad")
            precio = request.form.get("precio")
            # En la tabla compania EXISTENTE, obtener el id de la compa
            compania = request.form.get("compania")
            # En la tabla intermediario EXISTENTE obtener el id interm
            compania = request.form.get("intermediario")
            
            config.CUD(
                "INSERT INTO tasks (nombre, cantidad, descripcion, email, fecha) VALUES (%s, %s, %s, %s, %s)",
                (nombre, cantidad, compania, precio, session["email"]),
            )
            return redirect(url_for("products.warehouse"))
    else:
        return redirect(url_for("auth.signin"))


@products.route("/warehouse")
def warehouse():
    if "email" in session:
        products = config.Read(
            "SELECT ID_PRODUCTO, NOMBRE, PRECIO_UNITARIO, EXISTENCIAS FROM dbo.Almacen WHERE dbo.Almacen.ESTATUS = 1"
        )
        return render_template("products/warehouse.html", products=products)
    else:
        return redirect(url_for("auth.signin"))


@products.route("/delete_product", methods=["POST"])
def delete_product():
    # Verificar si el usuario tiene una sesión activa
    if "email" in session:
        # Verificar si el método de solicitud es POST
        if request.method == "POST":
            # Obtener el ID del producto de los datos del formulario
            product_id = request.form.get("product_id")
            print("========================================\nDATOS OBTENIDOS>\n")
            print(f"Product_ID - {product_id}")
            print("========================================")
            config.CUD(
                "UPDATE dbo.Almacen SET ESTATUS = 0 WHERE ID_PRODUCTO = {}".format(product_id)
            )
            return redirect(url_for("products.managewarehouse"))
    # Si el usuario no tiene una sesión activa, redirigirlo a la página de inicio de sesión
    return redirect(url_for("auth.signin"))

@products.route("/search_product", methods=["GET", "POST"])
def search_product():
    if "email" in session:
        if request.method == "POST":
            search_term = request.form.get("search_term")
            products = config.Read(
                "SELECT ID_PRODUCTO, NOMBRE, PRECIO_UNITARIO, EXISTENCIAS FROM dbo.Almacen WHERE NOMBRE LIKE '%{}%' AND dbo.Almacen.ESTATUS = 1".format(
                    search_term
                )
            )
            return render_template("products/warehouse.html", products=products)
    else:
        return redirect(url_for("auth.signin"))


@products.route("/manage_warehouse", methods=["GET", "POST"])
def managewarehouse():
    if "email" in session:
        products = config.Read(
            "SELECT ID_PRODUCTO, NOMBRE, PRECIO_UNITARIO, EXISTENCIAS FROM dbo.Almacen WHERE dbo.Almacen.ESTATUS = 1"
        )
        members = config.Read(
            "SELECT Proveedor.ID_COMPANIA, ID_INTERMEDIARIO ,Proveedor.NOMBRE, Intermediario.NOMBRE, Intermediario.AP_PAT, Intermediario.AP_MAT FROM dbo.Proveedor INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA WHERE dbo.Proveedor.ESTATUS = 1 AND dbo.Intermediario.ESTATUS = 1"
        )
        if request.method == "POST":
            print("hola")
        return render_template(
            "products/manage-warehouse.html",
            products=products,
            members=members,
        )
    else:
        return redirect(url_for("auth.signin"))


@products.route("/manage_presentation")
def managepresentation():
    return render_template("products/manage-presentation.html")


@products.route("/manage_company")
def managecompany():
    if "email" in session:
        companias = config.Read(
            "SELECT Proveedor.ID_COMPANIA, Proveedor.NOMBRE, Intermediario.NOMBRE, Intermediario.AP_PAT, Intermediario.AP_MAT, Intermediario.TEL,  Intermediario.ID_INTERMEDIARIO FROM dbo.Proveedor INNER JOIN dbo.Intermediario ON Intermediario.ID_COMPANIA = Proveedor.ID_COMPANIA WHERE dbo.Proveedor.ESTATUS = 1 AND dbo.Intermediario.ESTATUS = 1"
        )
        return render_template("products/manage-company.html", companias=companias)
    else:
        return redirect(url_for("auth.signin"))


@products.route("/delete_company", methods=["POST"])
def delete_company():
    # Verificar si el usuario tiene una sesión activa
    if "email" in session:
        # Verificar si el método de solicitud es POST
        if request.method == "POST":
            # Obtener el ID del intermediario de los datos del formulario
            company_id = request.form.get("company_id")
            print("========================================\nDATOS OBTENIDOS>\n")
            print(f"company_id - {company_id}")
            print("========================================")
            config.CUD(
                """
                UPDATE dbo.Intermediario SET ESTATUS = 0 WHERE ID_COMPANIA = {};
                UPDATE dbo.Proveedor SET ESTATUS = 0 WHERE ID_COMPANIA = {};
                """.format(
                    company_id, company_id
                )
            )
            return redirect(url_for("products.managecompany"))
    # Si el usuario no tiene una sesión activa, redirigirlo a la página de inicio de sesión
    return redirect(url_for("auth.signin"))


@p.route("/welcomeuser")
def welcomeuser():
    if "email" in session:
        print("========================================\nSession>\n")
        print(session)
        return render_template("profile/welcome-user.html")
    else:
        return redirect(url_for("auth.signin"))


@p.route("/profile")
def profile():
    return render_template("profile/profile.html")


@sc.route("/shortcut")
def shortcut():
    return render_template("shortcut.html")


@sc.route("/settings")
def settings():
    return render_template("settings/settings.html")


@app.route("/signout")
def signout():
    if "email" in session:
        session.pop("email", None)
        print("CERRANDO SESSION...")
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
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

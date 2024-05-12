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
        return render_template("profile.weclomeuser", email=session["email"])
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print("========================================\nDATOS OBTENIDOS>\n")
        print("Email - {}".format(email))
        print("Password - {}".format(password))
        print("========================================")
        existing_email = config.Read(
            "SELECT * FROM dbo.Usuarios WHERE CORREO = '{0}'".format(email)
        )

        if not existing_email:
            # El correo electrónico no está registrado
            email_not_found = True
            print(
                "========================================\ncorreo electrónico no está registrado\n========================================"
            )
            return render_template(
                "auth/signin.html", email_not_found=email_not_found
            )
        
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


@auth.route("/signup", methods=["GET", "POST"])  # Altas
def signup():
    print("========================================\nRUTA-Signup\n")
    # Verificar si hay una dirreccion de correo dentro de session
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
        print("Name - {}".format(name))
        print("Lastname - {}".format(lastname))
        print("Email - {}".format(email))
        print("Password - {}".format(password))
        print("========================================")

        aux = lastname.split()
        if len(aux) >= 2:
            apellido_paterno = aux[0]  # El primer elemento es el apellido paterno
            apellido_materno = aux[-1]  # El último elemento es el apellido materno
        else:
            lastname_error = True

        existing_email = config.Read(
            "SELECT * FROM dbo.Usuarios WHERE CORREO = '{0}'".format(email)
        )

        existing_user = config.Read(
            "SELECT * FROM dbo.Usuarios WHERE NOMBRE = '{0}' AND AP_PAT = '{1}' AND AP_MAT = '{2}'".format(name, apellido_paterno, apellido_materno)
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

        # No hay ningun error
        else:
            # registrar en base de datos
            config.CUD(
                "INSERT INTO dbo.Usuarios (NOMBRE, AP_PAT , AP_MAT , CORREO , CONTRASENA, ESTATUS) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}' , 1)".format(
                    name, apellido_paterno, apellido_materno, email, password
                )
            )
            print("Renderizar auth/sigin")
            return url_for("auth.signin.html", registration_successful=True)
    else:
        return render_template("auth/signup.html")


# Define tu vista para el registro exitoso aquí
@app.route("/successful_registration")
def successful_registration():
    return render_template("auth/successful-registration.html")

@products.route("/create_product", methods=["POST"])
def create_product():
    if "email" in session:
        if request.method == "POST":
            nombre = request.form.get("nombre")
            cantidad = request.form.get("cantidad")
            compania = request.form.get("compania")
            precio = request.form.get("precio")
            config.CUD(
                "INSERT INTO tasks (nombre, cantidad, descripcion, email, fecha) VALUES (%s, %s, %s, %s, %s)", (nombre, cantidad , compalia,session['email'])
            )
            return redirect(url_for("products.warehouse"))
    else:
        return redirect(url_for("auth.signin"))

@products.route("/warehouse")
def warehouse():
    # solamente es la vista general de los productos, capaz tenga que actualizarla (re plantearla)
    # no veo necesario hacer algo por el momento más que muestre todos los productos
    if "email" in session:
        # wewewewewewe aqui de devuelvo una matriz?
        # yep, solo devuelve una matriz con todos los datos hasta el momento.
        # tecnicamente en todas devuelves una matriz, en la de companias si creo que debes hacer un producto carteasiano para mostrarlo todo
        # Correcto, checar en pagina
        products = config.Read(
            "select dbo.Almacen.ID_PRODUCTO,dbo.Almacen.NOMBRE,dbo.Almacen.PRECIO_UNITARIO, dbo.Almacen.EXISTENCIAS From dbo.Almacen"
        )
        return render_template("products/warehouse.html", products=products)
    else:
        return redirect(url_for("auth.signin"))


@products.route("/delete_product", methods=["POST"])
def delete_product():
    if "email" in session:
        if request.method == "POST":
            product_id = request.form.get("product_id")
            print("Producto eliminado con ID: {}".format(product_id))
            query_delete = "DELETE FROM dbo.Almacen WHERE ID_PRODUCTO = {}".format(product_id)
            config.CUD(query_delete)
            return redirect(url_for("products.warehouse"))
    else:
        return redirect(url_for("auth.signin"))


@products.route("/manage_warehouse")
def managewarehouse():
    # maneja todos los comproductos del almacen ya sea agregar nuevos productos, eliminarnos, editarlos
    # actualmente creo que el boton de eliminar no funciona (no hice referencia a que capture los datos de la fila en la que esta)
    # al boton de eliminar le ocurre lo mismo.
    # cuando ajusten el html para que se ingresen los datos en la base de datos y lo muestre la tabla, me dicen para empezar a ver que pedo con esa parte.
    if "email" in session:
        products = config.Read(
            "select dbo.Almacen.ID_PRODUCTO,dbo.Almacen.NOMBRE,dbo.Almacen.PRECIO_UNITARIO, dbo.Almacen.EXISTENCIAS From dbo.Almacen"
        )
        company = config.Read("select dbo.Proveedor.NOMBRE From dbo.Proveedor")
        if request.method == "POST":
            print("hola")
        return render_template(
            "products/Manage-warehouse.html", products=products, company=company
        )
        # Agregar productos
    else:
        return redirect(url_for("signin"))


@products.route("/manage_presentation")
# maneja la presenracion pues como te planteee una tabla de un unico campo (dos con el id)
# puede agregar, editar e eliminar presentaciones
def managepresentation():
    return render_template("products/manage-presentation.html")

@products.route("/manage_company")
def managecompany():
    # al igual que las anteriores busca manejar tanto las companias como los intermediados,
    # asocie la vista para que se vea la relacion entre la compañia y el intermediado
    # puede eliminar compania e intermediado actual, editar y crear.
    if "email" in session:
        companias = config.Read("select dbo.Proveedor.ID_COMPANIA,dbo.Proveedor.NOMBRE,dbo.Intermediario.NOMBRE,dbo.Intermediario.AP_MAT,dbo.Intermediario.AP_MAT,dbo.Intermediario.TEL From dbo.Proveedor inner join dbo.Intermediario on dbo.Intermediario.ID_COMPANIA = dbo.Proveedor.ID_COMPANIA")
        return render_template(
            "products/manage-company.html",
            companias=companias
        )
    else:
        return redirect(url_for("signin"))


@p.route("/welcomeuser")
def welcomeuser():
    return render_template("profile/welcome-user.html")


@p.route("/profile")
def profile():
    return render_template("profile/profile.html")


@sc.route("/shortcut")
def shortcut():
    return render_template("shortcut.html")


@sc.route("/settings")
def settings():
    return render_template("settings/settings.html")


# Sign-Out
@app.route("/Signout")
def Signout():
    if "email" in session:
        session.pop(
            "email", None
        )  # Eliminar la clave 'email' de la sesión si está presente
        print("CERRANDO SESSION...")
        return redirect("auth/signin")
    else:
        print("NO HAY SESSION")
    return redirect(url_for("auth/signin"))


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

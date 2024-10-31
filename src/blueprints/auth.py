# import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# import
from models.queries import Read, CUD
# importar config
from models.user import ModelUser, Usuario, mariadb
#
from extensions import login_manager
#
from flask_login import login_user, login_required, logout_user, current_user
#
from werkzeug.security import generate_password_hash
#
import re

# NOTAS:


auth = Blueprint("auth", __name__, url_prefix="/auth")


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


# region Iniciar sesión
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("profile.welcomeuser"))
    if request.method == "POST":
        user = Usuario(0, request.form["email"], request.form["password"])
        logged_user=ModelUser.login(user)
        if logged_user is not None:
            if logged_user.contraseña:
                login_user(logged_user)
                print(logged_user.id)
                print(logged_user.tipo_usuario)
                return redirect(url_for("profile.welcomeuser"))
            else:
                flash("Contraseña incorrecta", "error")
        else:
            flash("Correo no encontrado", "error")
    return render_template("auth/signin.html")


# region Registro de usuario
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # Errores
    email_found = False  # El email ya esta registrado
    user_found = False  #   El usuario ya ha sido encontradoin
    ErrorNombre = False
    ErrorAP_PAT = False
    ErrorAP_MAT = False
    # Otros booleanos
    registration_successful = False
    print("<#################### signup ####################")
    # Verificar si hay una dirección de correo dentro de la sesión
    if "email" in session:
        print(
            "#################### Session iniciada renderizar index.html ####################>"
        )
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
        existing_email = Read(
            """
            SELECT * 
            FROM proyecto.usuarios 
            WHERE CORREO = ?
            """,
            (email,),
        )
        print("CONSULTA USUARIO")
        # Consulta para verificar si existe el usuario en la BD
        existing_user = Read(
            """
            SELECT * 
            FROM proyecto.usuarios 
            WHERE NOMBRE = ? 
            AND AP_PAT = ? 
            AND AP_MAT = ?
            """,
            (name, apellido_paterno, apellido_materno),
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
            CUD(
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


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("profile.welcomeuser"))
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))  # Hash de la contraseña
        print("<-------------------- Conectando... --------------------")
        connection = None  # Inicializa connection como None
        try:
            # Conectar a la BD
            connection = mariadb.connect(**ADMIN_CONECTION)
            cursor = connection.cursor()
            
            # Define la consulta y los parámetros como una tupla plana
            query = "INSERT INTO usuarios (NOMBRE, CORREO, CONTRASENA, ESTATUS) VALUES (?, ?, ?, 1)"
            params = (name, email, password)  # Tupla plana

            cursor.execute(query, params)  # Pasar la tupla plana
            connection.commit()  # Confirmar los cambios en la base de datos
            print("<-------------------- Conexión exitosa -------------------->")
        except Exception as ex:
            print(f"<-------------------- Error: {ex} -------------------->")
        finally:
            if connection:  # Solo cierra si connection fue asignada
                connection.close()
                print("-------------------- Conexión finalizada -------------------->")
        flash("Registro exitoso", "success")
        return redirect(url_for("auth.signin"))
    return render_template("auth/signup.html")

# region Cerrar sesión
@login_required
@auth.route("/signout")
def signout():
    if current_user.is_authenticated:
        logout_user()
        flash("Sesión cerrada correctamente", "success")
        return redirect(url_for("auth.signin"))

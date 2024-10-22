# import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# import
from models.queries import Read, CUD
# importar config
from models.user import ModelUser, Usuario
#
from extensions import login_manager
#
from flask_login import login_user

# NOTAS:


auth = Blueprint("auth", __name__, url_prefix="/auth")


# region Iniciar sesión
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if "email" in session:
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
    if "email" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        CUD(
            "INSERT INTO usuarios (NOMBRE, CORREO, CONTRASENA, ESTATUS) VALUES (?, ?, ?, 1)",
            (name, email, password),
        )
        flash("Registro exitoso", "success")
        return redirect(url_for("auth.signin"))

    return render_template("auth/signup.html")

# region Cerrar sesión
@auth.route("/signout")

def signout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("auth.signin"))

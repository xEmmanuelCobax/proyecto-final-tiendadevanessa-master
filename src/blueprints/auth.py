# import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# import flask_login
from flask_login import login_user, logout_user, login_required
# import config
from config import Read, CUD, ADMIN_CONECTION, MANAGER_CONECTION, CASHIER_CONECTION
# importar config
from config import DevelopmentConfig, ModelUser, Usuario


# NOTAS:


auth = Blueprint("auth", __name__, url_prefix="/auth")


# region Iniciar sesión
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if "email" in session:
        return redirect(url_for("profile.welcomeuser"))

    if request.method == "POST":
        """
        email = request.form["email"]
        password = request.form["password"]
        """
        user = Usuario(0, request.form["email"], request.form["password"])
        logged_user=ModelUser.login(user)
        if logged_user is not None:
            if logged_user.contraseña:
                return redirect(url_for("profile.welcomeuser"))
            else:
                flash("Contraseña incorrecta", "error")
        else:
            flash("Correo no encontrado", "error")
        """
        if not existing_email:
            flash("Correo no encontrado", "error")
        else:
            print()
        
                elif existing_email[0][6] == password:
            session["email"] = existing_email[0][5]
            session["ES_ADMIN"] = bool(existing_email[0][8])
            session["name"] = (
                f"{existing_email[0][1]} {existing_email[0][2]} {existing_email[0][3]}"
            )
            return redirect(url_for("profile.welcomeuser"))
        else:
            flash("Contraseña incorrecta", "error")
        """
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

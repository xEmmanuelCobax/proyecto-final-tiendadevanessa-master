from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from config import Read, CUD, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

# NOTAS:


auth = Blueprint("auth", __name__, url_prefix="/auth")


# region Iniciar sesión
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if "email" in session:
        return redirect(url_for("profile.welcomeuser"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        existing_email = Read(
            "SELECT * FROM usuarios WHERE CORREO = ? AND ESTATUS = 1", (email,)
        )
        if not existing_email:
            flash("Correo no encontrado", "error")
        else:
            print()
        """
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

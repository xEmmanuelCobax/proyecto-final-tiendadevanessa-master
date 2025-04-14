# import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# import
from models.queries import CUD, Read
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
from config import ADMIN_CONECTION
import smtplib
import random
import string
import os

from datetime import datetime, timedelta


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


# region Validar correo
def send_password_reminder(email, username):
    try:
        # Configuración del servidor SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_user = "e8467388@gmail.com"  # Reemplaza con tu correo
        smtp_password = (
            "xaxk tnds cays jkgb"  # Reemplaza con tu contraseña de aplicación
        )

        # Crear el mensaje en formato HTML
        subject = "Recordatorio: Cambia tu contraseña"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <table style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <tr>
                    <td style="text-align: center; padding-bottom: 20px;">
                        <h2 style="color: #4CAF50;">Hola, {username}</h2>
                    </td>
                </tr>
                <tr>
                    <td style="font-size: 16px; line-height: 1.6; color: #333333; text-align: center;">
                        <p>Han pasado más de <strong>30 días</strong> desde que cambiaste tu contraseña.</p>
                        <p>Por favor, actualízala para mantener tu cuenta segura.</p>
                        <a href="https://Fynex.com/cambiar-contraseña" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: #ffffff; text-decoration: none; border-radius: 5px; margin-top: 20px;">Cambiar contraseña</a>
                    </td>
                </tr>
                <tr>
                    <td style="font-size: 12px; line-height: 1.6; color: #888888; text-align: center; padding-top: 20px;">
                        <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                        <p>Gracias,<br>El equipo de Fynex</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        # Crear el mensaje con encabezados adicionales
        message = f"Subject: {subject}\n"
        message += "MIME-Version: 1.0\n"
        message += "Content-Type: text/html; charset=utf-8\n"
        message += f"From: Fynex <{smtp_user}>\n"
        message += f"Reply-To: soporte@Fynex.com\n\n"
        message += html_body

        # Conectar al servidor SMTP y enviar el correo
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email, message.encode("utf-8"))
        server.quit()

        print(f"Correo de recordatorio enviado a {email}")
    except Exception as e:
        print(f"Error al enviar el correo de recordatorio: {e}")


# region Enviar código de verificación
def send_verification_code(email, code):
    try:
        # Configuración del servidor SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_user = "e8467388@gmail.com"  # Reemplaza con tu correo
        smtp_password = (
            "xaxk tnds cays jkgb"  # Reemplaza con tu contraseña de aplicación
        )

        # Crear el mensaje en formato HTML
        subject = "Código de verificación"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <table style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <tr>
                    <td style="text-align: center; padding-bottom: 20px;">
                        <h2 style="color: #4CAF50;">Hola,</h2>
                    </td>
                </tr>
                <tr>
                    <td style="font-size: 16px; line-height: 1.6; color: #333333; text-align: center;">
                        <p>Tu código de verificación es:</p>
                        <h1 style="color: #4CAF50; font-size: 36px; margin: 20px 0;">{code}</h1>
                        <p>Por favor, ingresa este código en la página de verificación para continuar.</p>
                    </td>
                </tr>
                <tr>
                    <td style="font-size: 12px; line-height: 1.6; color: #888888; text-align: center; padding-top: 20px;">
                        <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                        <p>Gracias,<br>El equipo de Fynex</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        # Crear el mensaje con encabezados adicionales
        message = f"Subject: {subject}\n"
        message += "MIME-Version: 1.0\n"
        message += "Content-Type: text/html; charset=utf-8\n"
        message += f"From: Fynex <{smtp_user}>\n"
        message += f"Reply-To: soporte@Fynex.com\n\n"
        message += html_body

        # Conectar al servidor SMTP y enviar el correo
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email, message.encode("utf-8"))
        server.quit()

        print(f"Código de verificación enviado a {email}")
        return True
    except Exception as e:
        print(f"Error al enviar el código de verificación: {e}")
        return False


# region Iniciar sesión
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("sales.addsalesworker"))
    if request.method == "POST":
        user = Usuario(0, request.form["email"], request.form["password"])
        logged_user = ModelUser.login(user)
        if logged_user is not None:
            if logged_user.contraseña:
                # Verificar si la contraseña necesita ser actualizada
                last_change = (
                    logged_user.last_password_change
                )  # Asegúrate de que este campo esté en el modelo
                if last_change:
                    # Si last_change ya es un objeto datetime.date, conviértelo a datetime para la comparación
                    last_change_date = datetime.combine(last_change, datetime.min.time())
                    if datetime.now() - last_change_date > timedelta(days=30):  # Más de 30 días
                        flash(
                            "Han pasado más de 30 días desde que cambiaste tu contraseña. Por favor, actualízala.",
                            "warning",
                        )
                        send_password_reminder(logged_user.correo, logged_user.nombres)

                # Generar y enviar el código de verificación
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                session['verification_code'] = code
                if send_verification_code(logged_user.correo, code):
                    session['temp_user_id'] = logged_user.id
                    return redirect(url_for("auth.verify_code"))
                else:
                    flash("Error al enviar el código de verificación", "danger")
            else:
                flash("Contraseña incorrecta", "danger")
        else:
            flash("Contraseña incorrecta", "danger")
    return render_template("auth/signin.html")

@auth.route("/verify_code", methods=["GET", "POST"])
def verify_code():
    # Verificar si el usuario tiene permiso para acceder a esta página
    if "verification_code" not in session:
        flash("No tienes permiso para acceder a esta página.", "danger")
        return redirect(url_for("auth.signin"))

    if request.method == "POST":
        code = request.form.get("code")
        if code == session.get("verification_code"):
            user_id = session.pop("temp_user_id", None)
            if user_id:
                logged_user = ModelUser.get_by_id(user_id)
                login_user(logged_user)
                session.pop("verification_code", None)  # Eliminar la variable de sesión
                return redirect(url_for("profile.welcomeuser"))
            else:
                flash("Error al verificar el usuario.", "danger")
        else:
            flash("Código de verificación incorrecto.", "danger")
    return render_template("auth/verify_code.html")


# region Registro de usuario
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # Errores
    email_found = False  # El email ya esta registrado
    user_found = False  # El usuario ya ha sido encontradoin
    ErrorNombre = False
    ErrorAP_PAT = False
    ErrorAP_MAT = False
    # Otros booleanos
    registration_successful = False
    print("<#################### signup ####################")
    # Verificar si hay una dirección de correo dentro de la sesión
    if current_user.is_authenticated:
        return redirect(url_for("profile.welcomeuser"))
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
            ADMIN_CONECTION,
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
            ADMIN_CONECTION,
        )
        print("========================================>")
        # Existe el correo en la base de datos
        if existing_email:
            email_found = True
        # Existe el usuario en la base de datos (checar la logica de esto)
        if existing_user:
            user_found = True
        # Cualquier error
        if existing_email or existing_user:
            flash("El correo electrónico ingresado ya está en uso", "warning")
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
                INSERT INTO proyecto.usuarios (NOMBRE, AP_PAT, AP_MAT, CORREO, CONTRASENA, ESTATUS, ID_ROL) 
                VALUES (?, ?, ?, ?, ?, 1, 3)
                """,
                (
                    name,
                    apellido_paterno,
                    apellido_materno,
                    email,
                    generate_password_hash(password),
                ),
                ADMIN_CONECTION,  # Tupla correctamente definida
            )
            print("========================================>")
            # Salio todo bien entonces
            registration_successful = True
            user = f"{name} {apellido_paterno} {apellido_materno} "
            print("#################### Renderizar auth/signin ####################>")
            flash(f"¡Gracias por registrarte, {user}!", "success")
            return render_template(
                "auth/signup.html", registration_successful=registration_successful
            )
    else:
        print("#################### Renderizar auth/signup.html ####################>")
        return render_template("auth/signup.html")


# region Cerrar sesión
@login_required
@auth.route("/cerrar_sesion")
def cerrar_sesion():
    if current_user.is_authenticated:
        logout_user()
        flash("Sesión cerrada correctamente", "success")
        return redirect(url_for("auth.signin"))

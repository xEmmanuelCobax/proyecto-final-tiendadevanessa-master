# import flask
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# importar modelos para query
from models.queries import (
    Read,
    CUD,
    ConsultaPIA,
    ConsultaCompanias,
    ConsultaIntermediarios,
)
# importar las excepciones
from models.exceptions import MyException
# importar las extenciones
from extensions import login_manager
#
from flask_login import current_user, login_required

# NOTAS:


accounts = Blueprint("accounts", __name__, url_prefix="/accounts")


# region Manejar cuentas
@accounts.route("/manage_accounts", methods=["GET", "POST"])
@login_required
def manage_accounts():
    # Capa 1: Verificar si el usuario está autenticado
    if current_user.is_authenticated:
        tipo_usuario = current_user.get_tipo_usuario()
        # Capa 2: Verificar si el usuario es administrador
        if tipo_usuario not in ["Admin", "Gerente"]:
            # Redirige a la URL anterior o a una página por defecto
            flash("Esta seccion es solo para gerentes o administradores", "danger")
            return redirect(request.referrer or url_for("products.warehouse"))

        # Capa 3: Manejar la lógica del formulario POST
        if request.method == "POST":
            action = request.form.get("action")
            # region Borrar cuenta
            if action == "delete":
                try:
                    print("<#################### delete ####################")
                    id_intermediario = int(
                        request.form.get("DeleteIntermediaryId"))
                    print(f"id para eliminar usuarios - {id_intermediario}")
                    CUD(
                        """
                        -- Actualizar proyecto.usuarios
                        UPDATE proyecto.usuarios
                        SET ESTATUS = 0
                        WHERE ID_USUARIO = ?;
                        """,
                        (int(id_intermediario),),
                    )
                except Exception as e:
                    print(f"Type : {e}")
                    flash(f"Type : {e}")
                    print(
                        "#################### FIN (Error al borrar intermediario) ####################>"
                    )
            # region Editar cuenta
            elif action == "edit":
                try:
                    # Obtener datos del formulario, incluido company_id
                    nombre = request.form.get("editIntermediaryName")
                    apellido_paterno = request.form.get("NEW-AP_PAT")
                    apellido_materno = request.form.get("NEW-AP_MAT")
                    correo = request.form.get("NEW-Correo")
                    id_usuario = int(
                        request.form.get("EditIntermediary_id")
                    )  # Se obtiene de un dato oculto
                    # Pruebas
                    print("<==================== DATOS OBTENIDOS ====================")
                    print(f"nombre - {nombre}")
                    print(f"apellido_paterno - {apellido_paterno}")
                    print(f"apellido_materno - {apellido_materno}")
                    print(f"correo - {correo}")
                    print(f"id_usuario - {id_usuario}")
                    print("========================================>")
                    # Consulta para verificar si existe el correo en la BD
                    existing_email = Read(
                        """
                        SELECT * 
                        FROM proyecto.usuarios 
                        WHERE proyecto.usuarios.CORREO = ?
                        AND proyecto.usuarios.ID_USUARIO != ?
                        """,
                        (correo, int(id_usuario)),
                    )
                    # Consulta para verificar si existe el usuario en la BD
                    existing_user = Read(
                        """
                        SELECT * 
                        FROM proyecto.usuarios 
                        WHERE proyecto.usuarios.NOMBRE = ?
                        AND proyecto.usuarios.AP_PAT = ?
                        AND proyecto.usuarios.AP_MAT= ?
                        AND proyecto.usuarios.ID_USUARIO != ?
                        """,
                        (nombre, apellido_paterno,
                         apellido_materno, int(id_usuario)),
                    )
                    # Cualquier error
                    if existing_email or existing_user:
                        if existing_email and existing_user:
                            raise MyException(
                                "ErrorEditAccounts",
                                "El correo electronico y usuario ya existe en la base de datos.",
                            )
                        elif existing_email:
                            raise MyException(
                                "ErrorEditAccounts",
                                "El correo electronico ya existe en la base de datos.",
                            )
                        elif existing_user:
                            raise MyException(
                                "ErrorEditAccounts",
                                "El usuario ya existe en la base de datos.",
                            )
                    else:
                        # Actualizar en la base de datos
                        CUD(
                            """
                            UPDATE proyecto.usuarios 
                            SET NOMBRE=?, AP_PAT=?, AP_MAT=?, CORREO=?
                            WHERE ID_USUARIO = ?
                            """,
                            (
                                nombre,
                                apellido_paterno,
                                apellido_materno,
                                correo,
                                int(id_usuario),
                            ),
                        )
                        flash("Se ha actualizado correctamente los datos.")
                        print("Se ha actualizado correctamente los datos.")
                        print("#################### FIN ####################>")
                except MyException as ex:
                    Tipo, Mensaje = ex.args
                    print(f"Type {Tipo} : {Mensaje}")
                    flash(f"{Mensaje}")
                    print(
                        "#################### FIN (No se inserto F) ####################>"
                    )
                except Exception as e:
                    print(f"Type : {e}")
                    flash(f"{e}")
                    print(
                        "#################### FIN (No se inserto FX2) ####################>"
                    )
        # region Datos
        relations = []
        relations = Read(
            """
            SELECT
                usuarios.ID_USUARIO,
                usuarios.NOMBRE,
                usuarios.AP_PAT,
                usuarios.AP_MAT,
                usuarios.CORREO,
                usuarios.ESTATUS,
                roles.NOMBRE_ROL
            FROM
                proyecto.usuarios
            JOIN
                proyecto.roles ON usuarios.ID_ROL = roles.ID_ROL
            WHERE
                usuarios.ESTATUS = 1
                AND usuarios.ID_ROL = 3;

            """
        )
        print(
            "#################### products/manage-intermediary.html ####################>"
        )
        # region render
        return render_template(
            "accounts/manage-accounts.html",
            relations=relations,
            companies=ConsultaCompanias(),
        )
    return render_template("auth/signin.html")


@accounts.route('/editar_datos_cuenta')
@login_required
def editar_datos_cuenta():
    usuario_id = session.get('usuario_id', None)
    print("El correo en sesión es:", usuario_id)

    # Verificar si el correo está en la sesión
    if usuario_id is None:
        flash("No se ha encontrado el correo en la sesión.", "error")
        return redirect(url_for('auth.signin'))

    # Obtener los datos de la cuenta
    try:
        informacion_perfil = Read(
            """
            SELECT
            	usuarios.ID_USUARIO,
                usuarios.NOMBRE,
                usuarios.AP_PAT,
                usuarios.AP_MAT,
                usuarios.CORREO,
                usuarios.CONTRASENA
            FROM
                usuarios
            WHERE
                ID_USUARIO = %s;
            """,
            (usuario_id,)  # Usar el correo como parámetro
        )
    except Exception as e:
        flash(f"Error al consultar la base de datos: {e}", "error")
        return redirect(url_for('auth.signin'))

    print("Información del nutriólogo:", informacion_perfil)

    # Comprobar si se encontró al nutriólogo
    if not informacion_perfil:
        flash("No se encontró el nutriólogo.", "error")
        return redirect(url_for('auth.signin'))

    # Pasar la información correctamente a la plantilla
    return render_template("editar_cuenta.html", dato=informacion_perfil[0])


@accounts.route('/actualizar_cuenta', methods=['POST'])
@login_required
def actualizar_cuenta():

    if request.method == 'POST':
        nombres = str(request.form['nombres']).strip().lower()  # Minusculas
        ap_paterno = str(request.form['apellido_p']).strip().lower()
        ap_materno = str(request.form['apellido_m']).strip().lower()
        correo = str(request.form['correo']).strip().lower()
        indice_id = str(request.form['indice_id']).strip().lower()

        # Validar que el correo electrónico termine en ".com"
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[cC][oO][mM]$", correo):
            flash("El correo electrónico debe terminar en '.com'", "error_email")
            return redirect(url_for('editar_perfil'))

        # Comprobar si el correo ya está registrado
        try:
            correo_ya_existe = Read(
                """
                SELECT
                    *
                FROM
                    usuarios
                WHERE
                    CORREO = %s;
                    AND ID_USUARIO != %s;
                """,
                (correo, indice_id)  # Usar el correo como parámetro
            )

        except Exception as e:
            flash(f"Error al consultar la base de datos: {e}", "error")
            return redirect(url_for('index'))

        if correo_ya_existe:
            flash("El correo electrónico ya está registrado", "error_email")
            return redirect(url_for('accounts.editar_datos_cuenta'))

        else:
            # Actualizar los datos del usuario
            try:
                CUD(
                    """
                    UPDATE
                        usuarios
                    SET
                        NOMBRE = %s,
                        AP_PAT = %s,
                        AP_MAT = %s,
                        CORREO = %s
                    WHERE
                        ID_USUARIO = %s
                    """,
                    (nombres, ap_paterno, ap_materno, correo,
                     indice_id)  # Usar el correo como parámetro
                )
            except Exception as e:
                flash(f"Error al consultar la base de datos: {e}", "error")
                return redirect(url_for('accounts.editar_datos_cuenta'))
            # Actualizar la sesión
            session["email"] = correo
            flash("Perfil editado correctamente", "perfil_editado")
            return redirect(url_for('accounts.editar_datos_cuenta'))

    return redirect(url_for('accounts.editar_datos_cuenta'))

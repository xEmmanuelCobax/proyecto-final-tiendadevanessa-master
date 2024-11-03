# import flask
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
from flask_login import current_user

# NOTAS:


accounts = Blueprint("accounts", __name__, url_prefix="/accounts")


# region Manejar cuentas
@accounts.route("/manage_accounts", methods=["GET", "POST"])
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
                    id_intermediario = int(request.form.get("DeleteIntermediaryId"))
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
                        (nombre, apellido_paterno, apellido_materno, int(id_usuario)),
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
                proyecto.usuarios.ID_USUARIO,
                proyecto.usuarios.NOMBRE,
                proyecto.usuarios.AP_PAT,
                proyecto.usuarios.AP_MAT,
                proyecto.usuarios.CORREO 
            FROM proyecto.usuarios 
            WHERE proyecto.usuarios.ESTATUS = 1 
            AND proyecto.usuarios.ID_ROL = 3
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

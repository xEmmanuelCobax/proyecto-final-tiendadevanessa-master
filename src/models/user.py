# import mariadb
from flask import flash
import mariadb
# import flask_login
from flask_login import UserMixin
from platformdirs import user_log_dir
# import config
from config import ADMIN_CONECTION, MANAGER_CONECTION, CASHIER_CONECTION
# import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

from db import CUD


# NOTAS:

# region clase usuario
class Usuario(UserMixin):
    def __init__(
        self,
        id,
        correo,
        contraseña,
        tipo_usuario="",
        nombres="",
        ap_pat="",
        ap_mat="",
        sesion=""
    ) -> None:
        super().__init__()
        self.id = id
        self.correo = correo
        self.contraseña = contraseña
        self.tipo_usuario = tipo_usuario
        self.nombres = nombres
        self.ap_pat = ap_pat
        self.ap_mat = ap_mat
        self.sesion = sesion
        if tipo_usuario == "Admin":
            self._conection = ADMIN_CONECTION
        elif tipo_usuario == "Gerente":
            self._conection = MANAGER_CONECTION
        elif tipo_usuario == "Cajero":
            self._conection = CASHIER_CONECTION
        else:
            self._conection = None
    # region is_active

    def is_active(self):
        return self.ESTATUS == 1
    # region is_anonymous

    def is_anonymous(self):
        return False
    # region metodos get

    def get_name(self):
        return f"{self.nombres} {self.ap_pat} {self.ap_mat}"

    def get_tipo_usuario(self):
        return self.tipo_usuario

    def get_sesion(self):
        return self.sesion

    def get_gmail(self):
        return f"{self.correo}"

    # region check_password
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)


# region Class ModelUser
class ModelUser:
    @classmethod
    def login(self, user):
        print("<-------------------- Conectando... -------------------->")
        connection = None
        try:
            connection = mariadb.connect(**ADMIN_CONECTION)
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    ID_USUARIO,
                    NOMBRE,
                    AP_PAT,
                    AP_MAT,
                    CORREO,
                    CONTRASENA,
                    NOMBRE_ROL,
                    ESTADO_SESION
                FROM usuarios, roles
                WHERE usuarios.ID_ROL = roles.ID_ROL
                AND ESTATUS = 1
                AND CORREO = %s
                """,
                (user.correo,),  # Reemplaza con el correo del usuario
            )
            rows = cursor.fetchall()
            if rows:
                # Asume que el correo es único y solo devuelve una fila
                row = rows[0]  # Primera fila
                print(
                    "<-------------------- Conexión exitosa (ModelUser) -------------------->")
                # Crear un objeto Usuario a partir de los datos de la fila
                logged_user = Usuario(
                    row[0],  # ID_USUARIO
                    row[4],  # CORREO
                    row[5],  # contraseña
                    row[6],  # NOMBRE_ROL
                    row[1],  # NOMBRE
                    row[2],  # AP_PAT
                    row[3],  # AP_MAT
                    row[7],  # sesion
                )

                print(f"Contraseña ingresada desde el form: {user.contraseña}")
                print(
                    "Contraseña (hash) almacenada en la base de datos:", row[5])
                # Validar la contraseña ingresada con el hash almacenado
                if Usuario.check_password(row[5], user.contraseña):

                    if row[7] == 1:  # Si el estado_sesion es True, hay una sesión activa
                        print(
                            'La sesión ya está activa. Por favor, cierra la sesión primero.', 'warning')
                        flash(
                            'La sesión ya está activa. Por favor, cierra la sesión primero.', 'warning')
                        return None

                    print(f"id es: {row[0]}")
                    CUD(
                        """
                        UPDATE usuarios
                        SET ESTADO_SESION = 1
                        WHERE ID_USUARIO = %s;
                                """,
                        (row[0],),
                        ADMIN_CONECTION
                    )
                    flash(f'Inicio de sesión exitoso como {Usuario.get_tipo_usuario}', 'success')
                    print("Contraseña correcta")
                    return logged_user
                else:
                    print("Contraseña incorrecta")
                    flash('la contraseña es incorrecta', 'warning')
                    return None

            else:
                print(
                    "<-------------------- Usuario no encontrado -------------------->"
                )
                return None
        except Exception as ex:
            print(f"<-------------------- Error: {ex} -------------------->")
            return None
        finally:
            if connection:
                connection.close()
                print("-------------------- Conexión finalizada -------------------->")

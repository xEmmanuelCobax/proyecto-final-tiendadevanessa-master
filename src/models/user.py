# import mariadb
import mariadb
# import flask_login
from flask_login import UserMixin
# import config
from config import ADMIN_CONECTION, MANAGER_CONECTION, CASHIER_CONECTION
# import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash


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
    ) -> None:
        super().__init__()
        self.id = id
        self.correo = correo
        self.contraseña = contraseña
        self.tipo_usuario = tipo_usuario
        self.nombres = nombres
        self.ap_pat = ap_pat
        self.ap_mat = ap_mat
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
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.ESTATUS == 1
    # region is_anonymous
    def is_anonymous(self):
        return False
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
                    NOMBRE_ROL
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
                print("<-------------------- Conexión exitosa -------------------->")
                # Crear un objeto Usuario a partir de los datos de la fila
                logged_user = Usuario(
                    row[0],  # ID_USUARIO
                    row[4],  # CORREO
                    Usuario.check_password(
                        row[5], user.contraseña
                    ),  # Verificar contraseña
                    row[6],  # NOMBRE_ROL
                    row[1],  # NOMBRE
                    row[2],  # AP_PAT
                    row[3],  # AP_MAT
                )
                return logged_user
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

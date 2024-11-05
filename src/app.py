from datetime import timedelta
from flask import Flask
from flask_login import LoginManager
# Importar los blueprints
from blueprints.accounts import accounts
from blueprints.auth import auth
from blueprints.main import main
from blueprints.products import products
from blueprints.profile import profile
from blueprints.sales import sales
from blueprints.shortcut import shortcut
# importar config
from config import DevelopmentConfig, config, ADMIN_CONECTION
# importar
from extensions import login_manager
#
from models.user import Usuario
#
import mariadb

from flask_socketio import SocketIO, emit
# NOTAS:


# Inicializar la app y configurar login manager
app = Flask(__name__)
# Configuración de Flask-Login
login_manager.init_app(app)
socketio = SocketIO(app)


# Configuración
app.config["SECRET_KEY"] = DevelopmentConfig.SECRET_KEY
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
    minutes=10)  # Tiempo de sesión, ej. 5 minutos


# User loader
@login_manager.user_loader
def load_user(user_id):
    """Carga un usuario a partir de su ID."""
    connection = None
    try:
        connection = mariadb.connect(**ADMIN_CONECTION)
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT 
                    ID_USUARIO,
                    CORREO,
                    CONTRASENA,
                    NOMBRE_ROL,
                    NOMBRE,
                    AP_PAT,
                    AP_MAT
                FROM usuarios, roles 
                WHERE usuarios.ID_ROL = roles.ID_ROL 
                AND ESTATUS = 1
                AND ID_USUARIO = %s
            """,
            (user_id,),
        )

        row = cursor.fetchone()
        if row:
            return Usuario(
                row[0],  # ID_USUARIO
                row[1],  # CORREO
                "",  # Contraseña vacía, no se necesita
                row[3],  # NOMBRE_ROL
                row[4],  # NOMBRE
                row[5],  # AP_PAT
                row[6],  # AP_MAT
            )
        return None
    except Exception as ex:
        print(f"<-------------------- Error: {ex} -------------------->")
        return None
    finally:
        if connection:
            connection.close()

print(load_user)

# Registro de Blueprints
app.register_blueprint(accounts)
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(products)
app.register_blueprint(profile)
app.register_blueprint(shortcut)
app.register_blueprint(sales)

#
if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run(host="0.0.0.0", debug=True, port=8000)

from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO
from blueprints.accounts import accounts
from blueprints.auth import auth
from blueprints.main import main
from blueprints.products import products
from blueprints.profile import profile
from blueprints.sales import sales
from blueprints.shortcut import shortcut

from config import DevelopmentConfig, config, ADMIN_CONECTION
from extensions import login_manager
from models.user import Usuario
import mariadb
import logging
import time
from threading import Thread
from threading import Lock

# Bloqueo para proteger las variables globales
global_lock = Lock()

monkey.patch_all()

# Configuración básica de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# Inicializar la app y configurar login manager
app = Flask(__name__)
app.config["SECRET_KEY"] = DevelopmentConfig.SECRET_KEY
login_manager.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Middleware para registrar las direcciones IP de las solicitudes entrantes
@app.before_request
def log_request_info():
    logging.info(f"IP de la solicitud: {request.remote_addr}")

# Variables globales para el control de ventas y productos
sales_active_user = None  # Usuario activo realizando ventas
products_active_user = None  # Usuario activo gestionando productos
user_sessions = {}  # Diccionario para mapear user_id con request.sid

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
        logging.error(f"Error al cargar usuario: {ex}")
        return None
    finally:
        if connection:
            connection.close()

# Rutas y blueprints
app.register_blueprint(accounts)
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(products)
app.register_blueprint(profile)
app.register_blueprint(shortcut)
app.register_blueprint(sales)

# Variables globales para rastrear usuarios activos
sales_active_user = None  # Usuario activo en la página de ventas
products_active_user = None  # Usuario activo en la página de productos
user_sessions = {}  # Diccionario para mapear user_id con request.sid
last_heartbeat = {}  # Diccionario para rastrear el último ping de cada usuario

# Niveles de usuario
USER_LEVELS = {
    "Admin": 3,  # Nivel más alto
    "Gerente": 2,
    "Cajero": 1   # Nivel más bajo
}


# Evento para manejar usuarios activos en la página de ventas
@socketio.on("sales_page_active")
def sales_page_active(data):
    global sales_active_user, user_sessions
    user_id = data.get("user_id")
    user_role = data.get("user_role")

    if not user_id or not user_role:
        logging.error("Datos incompletos recibidos en sales_page_active.")
        socketio.emit(
            "error",
            {
                "message": "Datos incompletos. No se puede acceder a la página de ventas."
            },
            to=request.sid,
        )
        return

    with global_lock:  # Asegura acceso exclusivo a las variables globales
        # Si el usuario ya está registrado, actualiza su session_id
        if user_id in user_sessions:
            user_sessions[user_id] = request.sid
            logging.info(
                f"Usuario {user_id} recargó la página. Session ID actualizado."
            )
            return

        if not sales_active_user:  # Si no hay usuario activo
            sales_active_user = {"id": user_id, "role": user_role}
            user_sessions[user_id] = request.sid
            logging.info(
                f"Usuario {user_id} ({user_role}) accedió a la página de ventas."
            )
            socketio.emit(
                "lock_sales",
                {
                    "message": "Un usuario está gestionando ventas. Espere a que termine."
                },
                skip_sid=request.sid,
            )
        else:
            # Comparar niveles de usuario
            active_user = sales_active_user
            if (
                USER_LEVELS[user_role] > USER_LEVELS[active_user["role"]]
            ):  # Si el nuevo usuario tiene mayor nivel
                socketio.emit(
                    "unlock_sales",
                    {"message": "Has sido desplazado por un usuario con mayor nivel."},
                    to=user_sessions[active_user["id"]],
                )
                sales_active_user = {"id": user_id, "role": user_role}
                user_sessions[user_id] = request.sid
                logging.info(
                    f"Usuario {user_id} ({user_role}) desplazó al usuario {active_user['id']} ({active_user['role']}) en la página de ventas."
                )
            else:
                socketio.emit(
                    "lock_sales",
                    {
                        "message": "Un usuario con mayor nivel está gestionando ventas. Espere a que termine."
                    },
                    to=request.sid,
                )


@socketio.on("products_page_active")
def products_page_active(data):
    global products_active_user, user_sessions
    user_id = data.get("user_id")
    user_role = data.get("user_role")

    if not user_id or not user_role:
        logging.error("Datos incompletos recibidos en products_page_active.")
        socketio.emit(
            "error",
            {
                "message": "Datos incompletos. No se puede acceder a la página de productos."
            },
            to=request.sid,
        )
        return

    with global_lock:  # Asegura acceso exclusivo a las variables globales
        # Si el usuario ya está registrado, actualiza su session_id
        if user_id in user_sessions:
            user_sessions[user_id] = request.sid
            logging.info(
                f"Usuario {user_id} recargó la página. Session ID actualizado."
            )
            return

        if not products_active_user:  # Si no hay usuario activo
            products_active_user = {"id": user_id, "role": user_role}
            user_sessions[user_id] = request.sid
            logging.info(
                f"Usuario {user_id} ({user_role}) accedió a la página de productos."
            )
            socketio.emit(
                "lock_products",
                {
                    "message": "Un usuario está gestionando productos. Espere a que termine."
                },
                skip_sid=request.sid,
            )
        else:
            # Comparar niveles de usuario
            active_user = products_active_user
            if (
                USER_LEVELS[user_role] > USER_LEVELS[active_user["role"]]
            ):  # Si el nuevo usuario tiene mayor nivel
                socketio.emit(
                    "unlock_products",
                    {"message": "Has sido desplazado por un usuario con mayor nivel."},
                    to=user_sessions[active_user["id"]],
                )
                products_active_user = {"id": user_id, "role": user_role}
                user_sessions[user_id] = request.sid
                logging.info(
                    f"Usuario {user_id} ({user_role}) desplazó al usuario {active_user['id']} ({active_user['role']}) en la página de productos."
                )
            else:
                socketio.emit(
                    "lock_products",
                    {
                        "message": "Un usuario con mayor nivel está gestionando productos. Espere a que termine."
                    },
                    to=request.sid,
                )


# Evento para manejar el "heartbeat"
@socketio.on('heartbeat')
def handle_heartbeat(data):
    global last_heartbeat
    user_id = data.get('user_id')
    if user_id:
        last_heartbeat[user_id] = time.time()  # Registrar el tiempo actual
        logging.debug(f"Heartbeat recibido de usuario {user_id}")


# Evento para manejar desconexiones
@socketio.on("disconnect")
def disconnect_user():
    global sales_active_user, products_active_user, user_sessions, last_heartbeat
    sid = request.sid  # Obtén el Session ID del cliente desconectado
    for user_id, session_id in user_sessions.items():
        if session_id == sid:  # Verifica si el usuario desconectado es el activo
            if sales_active_user and sales_active_user["id"] == user_id:
                sales_active_user = None
                socketio.emit(
                    "unlock_sales",
                    {"message": "La página ahora está disponible."},
                    skip_sid=sid,
                )
                logging.info(
                    f"Usuario {user_id} se desconectó. Se desbloqueó la página de ventas."
                )
            elif products_active_user and products_active_user["id"] == user_id:
                products_active_user = None
                socketio.emit(
                    "unlock_products",
                    {"message": "La página ahora está disponible."},
                    skip_sid=sid,
                )
                logging.info(
                    f"Usuario {user_id} se desconectó. Se desbloqueó la página de productos."
                )
            user_sessions.pop(user_id, None)
            last_heartbeat.pop(user_id, None)
            break


# Hilo para monitorear usuarios inactivos
def monitor_heartbeats():
    global last_heartbeat, sales_active_user, products_active_user, user_sessions
    while True:
        current_time = time.time()
        inactive_users = []

        # Verificar usuarios inactivos
        for user_id, last_time in last_heartbeat.items():
            if current_time - last_time > 5:  # 5 segundos de inactividad
                inactive_users.append(user_id)

        # Liberar recursos para usuarios inactivos
        for user_id in inactive_users:
            last_heartbeat.pop(user_id, None)
            if sales_active_user and sales_active_user["id"] == user_id:
                sales_active_user = None
                socketio.emit('unlock_sales', {'message': 'La página ahora está disponible.'}, broadcast=True)
                logging.info(f"Usuario {user_id} inactivo. Se desbloqueó la página de ventas.")
            elif products_active_user and products_active_user["id"] == user_id:
                products_active_user = None
                socketio.emit('unlock_products', {'message': 'La página ahora está disponible.'}, broadcast=True)
                logging.info(f"Usuario {user_id} inactivo. Se desbloqueó la página de productos.")
            user_sessions.pop(user_id, None)

        time.sleep(1)  # Verificar cada segundo

# Iniciar el monitor de heartbeats en un hilo separado
heartbeat_thread = Thread(target=monitor_heartbeats, daemon=True)
heartbeat_thread.start()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000)

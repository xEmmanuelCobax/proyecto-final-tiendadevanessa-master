# NOTAS:


class config:
    SECRET_KEY = "d5fb8c4fa8bd46638dadc4e751e0d68d"


class DevelopmentConfig(config):
    DEGUB=True


config = {'development': DevelopmentConfig}

# Conexiones
ADMIN_CONECTION = {
    "host": "localhost",  # Cambia por tu host si es diferente
    "user": "Admin",  # Usuario de MariaDB
    "password": "123",  # Contraseña de MariaDB
    "database": "proyecto",  # Nombre de la base de datos
}

MANAGER_CONECTION = {
    "host": "localhost",  # Cambia por tu host si es diferente
    "user": "Gerente",  # Usuario de MariaDB
    "password": "123",  # Contraseña de MariaDB
    "database": "proyecto",  # Nombre de la base de datos
}

CASHIER_CONECTION = {
    "host": "localhost",  # Cambia por tu host si es diferente
    "user": "Cajero",  # Usuario de MariaDB
    "password": "123",  # Contraseña de MariaDB
    "database": "proyecto",  # Nombre de la base de datos
}

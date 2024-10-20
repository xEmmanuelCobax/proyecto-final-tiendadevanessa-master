import mariadb


# NOTAS:


class config:
    SECRET_KEY = "d5fb8c4fa8bd46638dadc4e751e0d68d"


class DevelopmentConfig(config):
    DEGUB=True


config = {'development': DevelopmentConfig}

# Conexiones
ADMIN_CONECTION = {
    "host": "localhost",  # Cambia por tu host si es diferente
    "user": "admin",  # Usuario de MariaDB
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


# region CUD
# CREATE, UPDATE Y DELETE
def CUD(query, params=None):
    print("<-------------------- Conectando... --------------------")
    try:
        # Conectar a la BD
        connection = mariadb.connect(
            host="localhost",  # Cambia por tu host si es diferente
            user="root",  # Usuario de MariaDB
            password="123",  # Contraseña de MariaDB
            database="proyecto",  # Nombre de la base de datos
        )
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()  # Confirmar los cambios en la base de datos
        print("<-------------------- Conexión exitosa --------------------")
    except Exception as ex:
        print(f"<-------------------- Error: {ex} -------------------->")
    finally:
        if connection:
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")

# region Read
def Read(query, params=None):
    print("<-------------------- Conectando... --------------------")
    connection = None
    try:
        connection = mariadb.connect(
            host="localhost",  # Cambia por tu host si es diferente
            user="root",  # Usuario de MariaDB
            password="123",  # Contraseña de MariaDB
            database="proyecto",  # Nombre de la base de datos
        )
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        results = [list(row) for row in rows]  # Convert each row to a list
        print("<-------------------- Conexión exitosa --------------------")
        for result in results:
            print(result)
        print("---------------------------------------->")
        return results
    except Exception as ex:
        results = False
        print(f"<-------------------- Error: {ex} -------------------->")
        return None
    finally:
        if connection:
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")

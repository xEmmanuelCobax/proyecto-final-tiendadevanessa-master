import mariadb
HEX_SEC_KEY = "d5fb8c4fa8bd46638dadc4e751e0d68d"

# Conexiones
ROOT_CONECTION = {
    "host": "localhost",  # Cambia por tu host si es diferente
    "user": "root",  # Usuario de MariaDB
    "password": "123",  # Contraseña de MariaDB
    "database": "braindamage",  # Nombre de la base de datos
}

MANAGER_CONECTION = {
    "host": "localhost",  # Cambia por tu host si es diferente
    "user": "Gerente",  # Usuario de MariaDB
    "password": "123",  # Contraseña de MariaDB
    "database": "braindamage",  # Nombre de la base de datos
}

CASHIER_CONECTION = {
    "host": "localhost",  # Cambia por tu host si es diferente
    "user": "Cajero",  # Usuario de MariaDB
    "password": "123",  # Contraseña de MariaDB
    "database": "braindamage",  # Nombre de la base de datos
}



# Metodo para poder realizar CUD> CREATE, UPDATE Y DELETE
def CUD(query, params=None, current_user=None):
    print("<-------------------- Conectando... --------------------")
    try:
        # Conectar a la BD
        connection = mariadb.connect(current_user.Conection)
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

# Metodo para poder leer consultas
def Read(query, params=None, current_user=None):
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

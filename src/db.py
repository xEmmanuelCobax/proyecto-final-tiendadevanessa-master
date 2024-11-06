import mariadb
#
from flask_login import current_user
#
from config import ADMIN_CONECTION

# current_user._conection

# NOTAS:
# estoy checando lo de usuarios


# region CUD
# CREATE, UPDATE Y DELETE
def CUD(query, params=None, CONECTION = None):
    print("<-------------------- Conectando... --------------------")
    connection = None  # Inicializa connection como None
    try:
        if CONECTION == None:
            # Conectar a la BD
            print(current_user._conection)
            connection = mariadb.connect(**current_user._conection)
            cursor = connection.cursor()
        else:
            connection = mariadb.connect(**CONECTION)
            cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()  # Confirmar los cambios en la base de datos
        last_id = cursor.lastrowid
        print(f"<-------------------- ID insertado: {last_id} -------------------->")
        print("<-------------------- Conexión exitosa --------------------")
        return last_id
    except Exception as ex:
        print(f"<-------------------- Error: {ex} -------------------->")
        return None
    finally:
        if connection:  # Solo cierra si connection fue asignada
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")


# region Read
def Read(query, params=None, CONECTION=None):
    print("<-------------------- Conectando... --------------------")
    connection = None
    try:
        if CONECTION == None:
            # Conectar a la BD
            print(current_user._conection)
            connection = mariadb.connect(**current_user._conection)
            cursor = connection.cursor()
        else:
            connection = mariadb.connect(**CONECTION)
            cursor = connection.cursor()
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

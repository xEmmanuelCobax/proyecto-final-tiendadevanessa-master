import mariadb
from flask_login import current_user
from config import ADMIN_CONNECTION


# region CUD
# CREATE, UPDATE Y DELETE
def CUD(query, params=None, CONNECTION=None):
    print("<-------------------- Conectando... --------------------")
    connection = None  # Inicializa connection como None
    try:
        if CONNECTION is None:
            # Conectar a la BD
            print(current_user._connection)
            connection = mariadb.connect(**current_user._connection)
        else:
            connection = mariadb.connect(**CONNECTION)
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        connection.commit()  
        print("<-------------------- Conexión exitosa --------------------")
    except Exception as ex:
        print(f"<-------------------- Error: {ex} -------------------->")
        if connection:
            connection.rollback()  
            print("<-------------------- Rollback realizado -------------------->")
    finally:
        if connection: 
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")


# region Read
def Read(query, params=None, CONNECTION=None):
    print("<-------------------- Conectando... --------------------")
    connection = None
    results = None  # Inicializa results como None para evitar referencias no deseadas
    try:
        if CONNECTION is None:
            # Conectar a la BD
            print(current_user._connection)
            connection = mariadb.connect(**current_user._connection)
        else:
            connection = mariadb.connect(**CONNECTION)

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

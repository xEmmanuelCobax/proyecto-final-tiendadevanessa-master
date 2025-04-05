import mariadb
from flask_login import current_user
from config import ADMIN_CONECTION
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')




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
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
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
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
        return None
    finally:
        if connection:
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")

# Region CallProcedure
def CallProcedure(procedure_name, params=None, CONNECTION=None):
    print(f"<-------------------- Llamando a {procedure_name} -------------------->")
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

        # Formar la consulta CALL del procedimiento
        if params:
            placeholders = ', '.join(['?'] * len(params))  # Genera ?, ?, ? según la cantidad de parámetros
            query = f"CALL {procedure_name}({placeholders})"
            cursor.execute(query, params)
        else:
            query = f"CALL {procedure_name}()"
            cursor.execute(query)

        rows = cursor.fetchall()
        results = [list(row) for row in rows]  # Convertir cada fila en una lista
        print("<-------------------- Procedimiento ejecutado con éxito -------------------->")
        for result in results:
            print(result)
        print("------------------------------------------------------------------------>")
        return results
    except Exception as ex:
        results = False
        print(f"<-------------------- Error: {ex} -------------------->")
        return None
    finally:
        if connection:
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")
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
             # Establecer el nivel de aislamiento a SERIALIZABLE
        connection.autocommit = False     
        cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        cursor.execute("SELECT @@tx_isolation;")

        current_isolation_level = cursor.fetchone()[0]
        print(f"El nivel de aislamiento actual es: {current_isolation_level}")
            # Iniciar la transacción
        cursor.execute("BEGIN")
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
        if connection:
            connection.rollback()
        return None
    finally:
        if connection:  # Solo cierra si connection fue asignada
            connection.close()
            print("-------------------- Conexión finalizada -------------------->")


# region Read
def Read(query, params=None, CONECTION=None, is_procedure=False ):
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

        if is_procedure:
            if params is None:
                params = []  # Asegura que params esté definido como lista vacía si no hay parámetros
            cursor.callproc(query, params)  # Ejecuta el procedimiento
            results = []
            for result in cursor.stored_results():
                rows = result.fetchall()
                results.extend([list(row) for row in rows])
        else:
            # Ejecuta una consulta normal
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            results = [list(row) for row in rows] # Convierte cada fila a lista


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

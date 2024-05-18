import pyodbc
HEX_SEC_KEY = "d5fb8c4fa8bd46638dadc4e751e0d68d"

# Metodo para poder realizar CUD> CREATE, UPDATE Y DELETE
def CUD(query):
    print("<-------------------- Conectando... --------------------")
    try:
        # Conectar a la BD DRIVER={SQL Server};SERVER=NOMBRE DEL SERVIDOR;DATABASE=NOMBRE DE LA BASE DE DATOS;Trusted_Connection=yes; EL TRUSTED ES PARA PODER CONECTAR SIN TENER CONTRASENAS
        connection = pyodbc.connect(
            "DRIVER={SQL Server};SERVER=PCEMMANUEL;DATABASE=Proyecto;Trusted_Connection=yes;"
        )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()  # Confirmar los cambios en la base de datos
        print("<-------------------- Conexión exitosa --------------------")
    except Exception as ex:
        print(f"<-------------------- Error: {ex} -------------------->")
    finally:
        connection.close()
        print("-------------------- Conexión finalizada -------------------->")


# Funcion para poder realizar consultas Read, devuelve UNA MATRIZ
def Read(query):
    print("<-------------------- Conectando... --------------------")
    try:
        connection = pyodbc.connect(
            "DRIVER={SQL Server};SERVER=PCEMMANUEL;DATABASE=Proyecto;Trusted_Connection=yes;"
        )
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        print("<-------------------- Conexión exitosa --------------------")
        for row in rows:
            print(row)
        print("---------------------------------------->")
        return rows
    except Exception as ex:
        print(f"<-------------------- Error: {ex} -------------------->")
    finally:
        connection.close()
        print("-------------------- Conexión finalizada -------------------->")

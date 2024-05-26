import re, config

def validar_entrada(texto):
    # a-z y A-Z son para minusculas y mayusculas
    # \u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00c1\u00c9\u00cd\u00d3\u00da\u00d1  Letras mayusculas y minusculas con acentos
    # \s Espacios en blanco
    # '' Al menos un caracter del conjunto
    # $ Al final de la cadena
    # Definimos el patrón que NO queremos en la entrada
    patron = r"^[a-zA-Z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00c1\u00c9\u00cd\u00d3\u00da\u00d1\s]+$"

    # Buscamos si hay alguna coincidencia en el texto
    if not re.search(patron, texto):
        return False
    else:
        return True


def validar_float(number):
    # Validar float y que sea un no negativo
    try:
        # Intentamos convertir el texto a un número flotante
        numero = float(number)
        # Comprobamos si el número es no negativo
        if numero >= 0:
            return True
        else:
            return False
    except ValueError:
        # Si ocurre un ValueError, el texto no es un número válido
        return False


def validar_float(texto):
    # Validar float y que sea un no negativo
    try:
        # Intentamos convertir el texto a un número flotante
        numero = int(texto)
        # Comprobamos si el número es no negativo
        if numero >= 0:
            return True
        else:
            return False
    except ValueError:
        # Si ocurre un ValueError, el texto no es un número válido
        return False


# Ejemplos de uso
entrada1 = "#$!!"
entrada2 = (123.2323)

print(validar_entrada(entrada1))  # Debería imprimir: True
print(validar_float(entrada2))  # Debería imprimir: False


def ConsultaProductos():
    auxiliar = []
    productos = []
    auxiliar = config.Read(
        """
        SELECT 
            ID_PRODUCTO, 
            NOMBRE, 
            PRECIO_UNITARIO, 
            EXISTENCIAS 
        FROM dbo.Almacen 
        WHERE dbo.Almacen.ESTATUS = 1
        """
    )
    for i in range(len(auxiliar)):
        if auxiliar[i][3] <= 0:
            print(int(auxiliar[i][0]))
            config.CUD(
                """
                UPDATE dbo.Almacen 
                    SET 
                    ESTATUS = ?
                WHERE ID_PRODUCTO = ?
                """,
                (0, int(auxiliar[i][0])),
            )
    productos = config.Read(
        """
        SELECT 
            ID_PRODUCTO, 
            NOMBRE, 
            PRECIO_UNITARIO, 
            EXISTENCIAS 
        FROM dbo.Almacen 
        WHERE dbo.Almacen.ESTATUS = 1
        """
    )
    return productos

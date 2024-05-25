import re

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
entrada1 = "123123123"
entrada2 = (123.2323)

print(validar_entrada(entrada1))  # Debería imprimir: True
print(validar_float(entrada2))  # Debería imprimir: False





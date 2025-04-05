from werkzeug.security import generate_password_hash

# Contraseña que quieres encriptar
password = "RaP1D0"

# Generar el hash de la contraseña
hashed_password = generate_password_hash(password)

# Imprimir el hash generado
print(f"Hash generado: {hashed_password}")

from werkzeug.security import generate_password_hash, check_password_hash

# Generar un hash para una contraseña
password = "12345"
hashed_password = generate_password_hash(password)

print("Contraseña Hasheada:", hashed_password)

# Verificar una contraseña contra el hash
password_verificada = check_password_hash(hashed_password, "12345")

if password_verificada:
    print("La contraseña es correcta.")
else:
    print("La contraseña es incorrecta.")

from werkzeug.security import generate_password_hash, check_password_hash
contraseña = generate_password_hash("123")
print(contraseña)

if check_password_hash(
    "scrypt:32768:8:1$p6YIyVfuDbsM85n8$3ec9a4a2ff4395d23af66aa270282d7185f14fe4fd63903bf95cebf628280f7b5add9a2eb7c6fefe504cbb85f3aa3cb1afb383a1b8205a50057cc9182c11d0d0",
    "123",
):
    print("Contraseña correcta")
else:
    print("Contraseña incorrecta")

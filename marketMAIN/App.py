import config

name = "Emmanuel"
apellido_paterno = "Coba"
apellido_materno = "Cuevas"
email = "emmanuelcobacuevas@gmail.com"
password = "123"

# Prubas
print("<==================== DATOS OBTENIDOS ====================")
print(f"Name - {name}")
print(f"apellido_paterno - {apellido_paterno}")
print(f"apellido_materno - {apellido_materno}")
print(f"Email - {email}")
print(f"Password - {password}")
print("========================================>")
# Consulta para verificar si existe el correo en la BD
existing_email = config.Read(
    """
    SELECT * 
    FROM proyecto.usuarios 
    WHERE CORREO = ?
    """,
    (email,),  # Asegúrate de que esté en forma de tupla
)

# Redondear con round()
num1 = 3.14159
print("Round:", round(num1))  # Salida: 3
print("Round to 2 decimals:", round(num1, 2))  # Salida: 3.14

# Redondear con ceil y floor
import math

print("Ceil:", math.ceil(num1))  # Salida: 4
print("Floor:", math.floor(num1))  # Salida: 3

# Truncar el número
print("Trunc:", math.trunc(num1))  # Salida: 3

# Redondear con decimal
from decimal import Decimal, ROUND_HALF_UP

num2 = Decimal("3.14159")
rounded_num2 = num2.quantize(Decimal("1.00"), rounding=ROUND_HALF_UP)
print("Decimal Round to 2 decimals:", rounded_num2)  # Salida: 3.14

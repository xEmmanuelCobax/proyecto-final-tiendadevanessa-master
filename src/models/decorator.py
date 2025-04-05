from functools import wraps
from flask import jsonify

# Variable global para rastrear el estado
sales_active_user = None

def block_sales_if_active(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global sales_active_user
        if sales_active_user:
            return jsonify({'error': 'Otro usuario está realizando ventas. Espere a que termine.'}), 403
        return f(*args, **kwargs)
    return decorated_function
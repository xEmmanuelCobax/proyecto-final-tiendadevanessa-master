from flask import Flask
# Importar los blueprints
from blueprints.accounts import accounts
from blueprints.auth import auth
from blueprints.main import main
from blueprints.products import products
from blueprints.profile import profile
from blueprints.sales import sales
from blueprints.shortcut import shortcut
# importar config
from config import DevelopmentConfig, config, Usuario
# importar flask_login
from flask_login import (
    login_manager,
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)

# NOTAS:

# Inicializar la app y configurar login manager
app = Flask(__name__)
# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.signin"


# Configuración
app.config["SECRET_KEY"] = DevelopmentConfig.SECRET_KEY


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Registro de Blueprints
app.register_blueprint(accounts)
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(products)
app.register_blueprint(profile)
app.register_blueprint(shortcut)
app.register_blueprint(sales)


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run(debug=True)

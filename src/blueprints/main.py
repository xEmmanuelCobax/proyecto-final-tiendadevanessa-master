# import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# importar modelos para query
from models.queries import (
    Read,
    CUD,
    ConsultaPIA,
    ConsultaCompanias,
    ConsultaIntermediarios,
)
# importar las excepciones
from models.exceptions import MyException
# importar las extenciones
from extensions import login_manager
#
from flask_login import login_user, logout_user, login_required, current_user

# NOTAS:


main = Blueprint("main", __name__)

# region Ruta Principal
@main.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    print("#################### NO HAY SESSION ####################>")
    return render_template("index.html")
# endregion

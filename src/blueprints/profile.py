from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# import flask_login
from flask_login import login_user, logout_user, login_required, current_user


# NOTAS:


profile = Blueprint("profile", __name__, url_prefix="/profile")


@profile.route("/welcomeuser")
@login_required
def welcomeuser():
    print("<#################### welcomeuser ####################")
    user = ""
    tipo = ""
    if current_user.is_authenticated:
        user = current_user.get_name()  # Obtener el nombre del usuario
        tipo = current_user.get_tipo_usuario()
    print("#################### FIN (profile/welcome-user.html) ####################>")
    return render_template(
        "profile/welcome-user.html",
        user=user,
        tipo=tipo
    )


# endregion

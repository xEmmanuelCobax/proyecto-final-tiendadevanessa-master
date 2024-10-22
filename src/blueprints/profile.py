from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# import flask_login
from flask_login import login_user, logout_user, login_required


# NOTAS:


profile = Blueprint("profile", __name__, url_prefix="/profile")


# region Bienvenida
@login_user
@profile.route("/welcomeuser")
def welcomeuser():
    # Errores
    print("<#################### welcomeuser ####################")
    
    print("Session > ", session)
    print("Nombre > ", session["name"])
    print("Es admin? > ", session["ES_ADMIN"])
    print("#################### FIN (profile/welcome-user.html) ####################>")
    return render_template(
        "profile/welcome-user.html",
        user=session["name"],
        IsAdmin=session["ES_ADMIN"],
    )
# endregion

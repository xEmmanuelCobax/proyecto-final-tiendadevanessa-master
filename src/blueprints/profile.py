from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# import flask_login
from flask_login import login_user, logout_user, login_required, current_user


# NOTAS:


profile = Blueprint("profile", __name__, url_prefix="/profile")


# region Bienvenida
@profile.route("/welcomeuser")
@login_required
def welcomeuser():
    # Errores
    print("<#################### welcomeuser ####################")
    if current_user.is_authenticated:
        
        return render_template("welcome.html", user=current_user)
    print("#################### FIN (profile/welcome-user.html) ####################>")
    return render_template(
        "profile/welcome-user.html",
        user=session["name"],
        IsAdmin=session["ES_ADMIN"],
    )
# endregion

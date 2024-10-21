from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import config, models


# NOTAS:


profile = Blueprint("profile", __name__, url_prefix="/profile")


# region Bienvenida
@profile.route("/welcomeuser")
def welcomeuser():
    # Errores
    print("<#################### welcomeuser ####################")
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
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

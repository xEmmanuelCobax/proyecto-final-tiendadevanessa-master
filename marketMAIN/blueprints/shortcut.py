from flask import Blueprint, render_template, request, redirect, url_for, flash, session


# NOTAS:


shortcut = Blueprint("shortcut", __name__, url_prefix="/shortcut")


# region Ajustes
@shortcut.route("/settings")
def settings():
    return render_template("settings/settings.html")
# endregion

# region ShortCut
@shortcut.route("/shortcut")
def shortcuts():
    # Errores
    print("<#################### index ####################")
    # Capa 1: Verificar si el usuario está autenticado
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return redirect(url_for("index"))
    print("#################### FIN RenderT(index.html) ####################>")
    return render_template("shortcut.html", IsAdmin=session["ES_ADMIN"])
# endregion

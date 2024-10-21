from flask import Blueprint, render_template, session, redirect, url_for


# NOTAS:


main = Blueprint("main", __name__)


# region Ruta Principal
@main.route("/")
def index():
    # Errores
    if "email" not in session:
        print("#################### NO HAY SESSION ####################>")
        return render_template("index.html")
    print("#################### FIN RenderT(index.html) ####################>")
    return render_template("index.html")

    # return redirect(url_for("shortcut.shortcuts"))

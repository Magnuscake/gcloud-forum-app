from flask import Blueprint, render_template, request, flash

from .datastore.user import user_exists

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form

        user_id = data.get("userId")
        password = data.get("password")

        found_user = user_exists(user_id, password)

        if found_user:
            flash("Login successful", category="success")
        else:
            flash("ID or password is invalid", category="error")


    return render_template("login.html")

@auth.route("/signup")
def signup():
    return render_template("signup.html")

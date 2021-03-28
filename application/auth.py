from flask import Blueprint, render_template, request, redirect, url_for, flash

from .datastore.user import user_exists, create_new_user

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
            return redirect(url_for('views.home'))
        else:
            flash("ID or password is invalid", category="error")


    return render_template("login.html")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form

        user_id = data.get("userId")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        if (len(user_id) < 2):
            flash("Please enter a valid user ID")
        elif (len(username) < 3):
            flash("Please enter a valid username")
        if (password1 != password2):
            flash("Passwords do not match", category="error")
        else:
            create_new_user(user_id, username, password1)
            flash("Account has been successfully been created")
    return render_template("signup.html")

from flask import Blueprint, render_template, request, redirect, url_for, flash

from .datastore import user_exists_login, create_new_user, property_is_unique

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form

        user_id = data.get("userId")
        password = data.get("password")

        found_user = user_exists_login(user_id, password)

        if found_user:
            flash("Login successful", category="success")
            return redirect(url_for('views.home'))
        else:
            flash("ID or password is invalid", category="error")


    return render_template("login.html")

# TODO: Uploading image functionality
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form

        user_id = data.get("userId")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        if (user_id and len(user_id) < 2):
            flash("Please enter a valid user ID", category="error")
        elif (username and len(username) < 3):
            flash("Please enter a valid username", category="error")
        # Uniquness checks
        elif (property_is_unique('id', user_id)):
            flash("This ID already exists", category="error")
        elif (property_is_unique('user', username)):
              flash("This username already exists", category="error")

        elif (password1 != password2):
            flash("Passwords do not match", category="error")
        else:
            create_new_user(user_id, username, password1)
            flash("Account has been successfully been created")
            return redirect(url_for('auth.login'))

    return render_template("signup.html")

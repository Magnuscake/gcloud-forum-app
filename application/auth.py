from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session
)

from .datastore import user_exists_login, create_new_user, property_is_unique
from .cloud_storage import upload_image

auth = Blueprint('auth', __name__)

# Routes
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form

        user_id = data.get('userId')
        password = data.get('password')

        found_user, key = user_exists_login(user_id, password)

        if found_user:
            flash("Login successful", category='success')
            # Pack all user info into a dictionary
            user_session_info = {
                'username': found_user,
                'user_id': user_id,
                'key': key
            }

            session['user_info'] = user_session_info
            session['logged_in'] = True

            return redirect(url_for('views.home'))

        else:
            flash("ID or password is invalid", category='error')

    return render_template('login.html', title="Login")

@auth.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form

        user_id = data.get('userId')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')
        image = request.files.get('image')

        if (user_id and len(user_id) < 2):
            flash('Please enter a valid user ID', category='error')
        elif (username and len(username) < 3):
            flash('Please enter a valid username', category='error')

        # Uniquness checks
        elif (property_is_unique('id', user_id)):
            flash("This ID already exists", category="error")
        elif (property_is_unique('user_name', username)):
              flash("This username already exists", category="error")

        elif (password1 == '' or password2 == ''):
            flash("Please enter a valid password", category='error')
        elif (password1 != password2):
            flash("Passwords do not match", category='error')
        else:
            if image.filename != '':
                upload_image('cc-user_profile_picture', image, user_id)

            create_new_user(user_id, username, password1)
            flash("Account has been successfully been created", category='success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html', title="Sign Up")

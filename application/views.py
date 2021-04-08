from functools import wraps

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash, session
)

from .datastore import create_new_message, get_all_messages, get_user_messages, update_password

views = Blueprint('views', __name__)

nav =[
    {'name': "View Messages", 'url': "/messages"},
    {'name': "New Message", 'url': "/new-message"},
    {'name': "Logout", 'url': "/logout"},
]

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap

# Routes
@views.route('/')
def redirect_to_login():
    return redirect(url_for('auth.login'))

@views.route('/forum')
@login_required
def home():
    return render_template('home.html', username=session['username'], nav=nav, title="Welcome to the forum")

@views.route('/messages')
@login_required
def messages():
    messages = get_all_messages()
    return render_template('messages.html', messages=messages, nav=nav, title="View Messages")

@views.route('/new-message', methods=['GET', 'POST'])
@login_required
def new_message():
    if request.method == 'POST':
        data = request.form

        subject = data.get('subject')
        message_text = data.get('messageText')

        if (not subject):
            flash("Please enter a valid subject", category='error')
        else:
            create_new_message(subject, message_text, session['username'], session['key'])
            flash("Your message has been successfully posted")

    return render_template('new-message.html', nav=nav, title="Post New Message")

@views.route('/user-page', methods=['GET', 'POST'])
def user_page():
    if request.method == 'POST':
        data = request.form

        user_id = session.get('userId')
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')

        updated = update_password(user_id, old_password, new_password)

        if (updated):
            flash("Password has been successfully changed", category="success")
        else:
            flash("Current password does not match", category="error")

    user_messages = get_user_messages(session['key'])

    return render_template('user-page.html', nav=nav, messages=user_messages)

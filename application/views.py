from functools import wraps
import string
import random
import time

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash, session
)

from .datastore import (
    create_new_message, get_all_messages, get_single_message, get_user_messages, update_password, update_message
)
from .cloud_storage import retrive_image, upload_image

views = Blueprint('views', __name__)

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap

# Helpers
def generate_filename():
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(10))

    return random_str

# Routes
@views.route('/')
def redirect_to_login():
    return redirect(url_for('auth.login'))

@views.route('/forum')
@login_required
def home():
    image_src = retrive_image('cc-user_profile_picture', session['user_info']['user_id'])
    return render_template('home.html', username=session['user_info']['username'], title="Welcome to the forum", image_src=image_src) 

@views.route('/messages')
@login_required
def messages():
    messages = get_all_messages()
    return render_template('messages.html', messages=messages, title="View Messages")

@views.route('/new-message', methods=['GET', 'POST'])
@login_required
def new_message():
    if request.method == 'POST':
        data = request.form

        subject = data.get('subject')
        message_text = data.get('messageText')
        image = request.files.get('image')

        if not subject:
            flash("Please enter a subject for you message", category='error')
        else:
            img_url = ''

            if image.filename != '':
                destination_file_name = f"{session['user_info']['user_id']}_{generate_filename()}"

                img = upload_image('cc-message_images', image, destination_file_name)

                img_url = f"https://storage.googleapis.com/cc-message_images/{img}"


            create_new_message(
                subject,
                message_text, 
                session['user_info']['username'], 
                session['user_info']['key'],
                img_url
            )
            flash("Your message has been successfully posted")
            return redirect(url_for('.messages'))

    return render_template('new-message.html', title="Post New Message")

@views.route('/user-page', methods=['GET', 'POST'])
def user_page():
    if request.method == 'POST':

        if not request.form.get('message-id'):
            data = request.form

            user_id = session['user_info']['key']
            old_password = data.get('oldPassword')
            new_password = data.get('newPassword')

            if (not new_password or len(new_password) <= 2):
                print('here')
                flash("Please enter a valid new password", category="error")
            else:
                updated_is_password = update_password(user_id, old_password, new_password)

                if (updated_is_password):
                    flash("Password has been successfully changed", category='success')
                    return redirect(url_for('auth.logout'))
                else:
                    flash("Current password does not match", category="error")

        else:
            #  message_key = request.get_json()['key']
            #  message = get_single_message(message_key, session['user_info']['key'])
            #  print(message_key)
            #  session['message_info'] = message
            #  return redirect(url_for('.edit_message'))
            message_key = request.form.get('message-id')
            message = get_single_message(message_key, session['user_info']['key'])
            session['message_info'] = message
            session['message_info']['key'] = message.key.id
            return redirect(url_for('.edit_message'))

    user_messages = get_user_messages(session['user_info']['key'])

    return render_template('user-page.html', messages=user_messages)

@views.route('/edit-message', methods=['GET', 'POST'])
def edit_message():
    if request.method == 'POST':
        data = request.form

        subject = data.get('subject')
        message_text = data.get('messageText')
        image = request.files.get('image')

        if not subject:
            flash("Please enter a subject for you message", category='error')

        update_message(
            session['message_info']['key'],
            session['user_info']['key'],
            session['user_info']['username'],
            session['message_info']['img_url'],
            subject,
            message_text,
        )
        flash("Your message has been successfully edited")
        return redirect(url_for('.user_page'))

    return render_template('edit-message.html', message=session['message_info'])

from flask import Blueprint, render_template, redirect, url_for

views = Blueprint('views', __name__)

@views.route('/')
def redirect_to_login():
    return redirect(url_for('auth.login'))

@views.route('/forum')
def home():
    return render_template("home.html")

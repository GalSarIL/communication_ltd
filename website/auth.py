from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Username does not exists', category="error")
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(username=username).first()
        email = User.query.filter_by(email=email).first()
        if user:
            flash('Username already exists.', category='error')
        elif email:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Incorrect Email', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User created!', category='success')
            return redirect(url_for('views.home'))

    return  render_template("sign_up.html")
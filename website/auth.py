from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .pw_configuration import password_check

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
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Username does not exists', category="error")
    return render_template("login.html", user=current_user)


@auth.route('/change-pw', methods=['GET', 'POST'])
def change_pw():
    if request.method == 'POST':
        password = request.form.get('password')
        newPassword1 = request.form.get('newPassword1')
        newPassword2 = request.form.get('newPassword2')

        user = User.query.filter_by(username=current_user.username).first()
        if check_password_hash(user.password, password):
            if newPassword1 != newPassword2:
                flash('Passwords does not match!', category='error')
            elif password_check(newPassword1):
                user.password = password = generate_password_hash(newPassword1, method='sha256')
                db.session.commit()
                flash('Password changed successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Please try again', category='error')
        else:
            flash('Incorrect password, try again', category='error')
    return render_template("change_pw.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        userChecker = User.query.filter_by(username=username).first()
        emailChecker = User.query.filter_by(email=email).first()
        if userChecker:
            flash('Username already exists.', category='error')
        elif emailChecker:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Incorrect Email', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif not password_check(password1):
            flash('Please try again', category='error')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        newPassword1 = request.form.get('newPassword1')
        newPassword2 = request.form.get('newPassword2')

        user = User.query.filter_by(username=current_user.username).first()
        if newPassword1 != newPassword2:
            flash('Passwords does not match!', category='error')
        elif password_check(newPassword1):
            user.password = generate_password_hash(newPassword1, method='sha256')
            db.session.commit()
            flash('Password changed successfully!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Please try again', category='error')
    return render_template("reset_password.html", user=current_user)

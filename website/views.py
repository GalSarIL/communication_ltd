from flask import Blueprint, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user, login_user
from werkzeug.utils import redirect
from .models import Customer, User
from . import db
import json, datetime
from website import app
from flask_mail import Message, Mail

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        customerName = request.form.get('customerName')
        customerPackage = request.form.get('customerPackage')
        tmp = request.form.get('customerDOJ')
        customerDOJ = datetime.datetime.strptime(tmp, '%Y-%m-%d').date()
        if len(customerName) < 1:
            flash('Customer name must be atleast 2 characters', category='error')
        elif customerPackage is None:
            flash('You must specify the package name', category='error')
        elif customerDOJ is None:
            flash('You must specify date of customer join', category='error')
        else:
            new_customer = Customer(customerName=customerName, customerPackage=customerPackage, customerDOJ=customerDOJ,
                                    user_id=current_user.id)
            db.session.add(new_customer)
            db.session.commit()
            flash('Customer added!', category='success')
    return render_template("home.html", user=current_user)


@views.route('/delete-customer', methods=['POST'])
def delete_customer():
    customer = json.loads(request.data)
    customerId = customer['customerId']
    customer = Customer.query.get(customerId)
    if customer:
        if customer.user_id == current_user.id:
            db.session.delete(customer)
            db.session.commit()
    return jsonify({})


def send_reset_email(user):
    mail = Mail(app)
    token = user.encode_auth_token(user.id)
    msg = Message('Password Reset Request',
                  sender='my.comm.comp@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    
    {url_for('views.reset_token', token=token, _external=True)}
    
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


@views.route('/reset_request', methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('There is no account with that email. You must register first.', category='error')
        else:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', category='success')
    return render_template('reset_request.html', user=current_user)


@views.route('/reset-request/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user_id = User.decode_auth_token(token)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('That is an invalid or expired token', category='error')
        return redirect(url_for('views.reset_request'))
    login_user(user, remember=True)
    return redirect(url_for('auth.reset_password'))

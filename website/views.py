from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Customer
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        customerName = request.form.get('customerName')
        customerPackage = request.form.get('customerPackage')
        customerDOJ = request.form.get('customerDOJ')
        print("START")
        print(request.form)
        print("END")
        if len(customerName) < 1:
            flash('Customer name must be atleast 2 characters', category='error')
        elif customerPackage is None:
            flash('You must specify the package name', category='error')
        elif customerDOJ is None:
            flash('You must specify date of customer join', caterogy='error')
        else:
            new_customer = Customer(customerName=customerName, customerPackage=customerPackage, customerDOJ=customerDOJ, user_id=current_user.id)
            db.serssion.add(new_customer)
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

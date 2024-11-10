from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from .cust_service import signup as signup_service,login as login_service, logout as logout_service, update_customer_profile, getCustomer,update_avatar_path
from library.model import Customer, Cart
from library.shopping.shop_service import CartService
from library.extension import db
customer = Blueprint("customer", __name__)

@customer.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response, status_code = signup_service(request.form) 
        
        if status_code == 200:  
            flash(response.get_json().get('message'), "success_signup")
            return redirect('/login')
        
        elif status_code == 400:
            flash(response.get_json().get('message'), "error_signup")
            return redirect('/signup')

        flash("An unknown error occurred", "error")
        return redirect('/signup')

    return render_template('signup.html')


@customer.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = login_service(request.form)  

        if response[1] == 200:  
            return redirect('/')  

        flash(response[0].json['message'], "error")  
        return redirect('/login')

    return render_template('login.html')


@customer.route('/logout')
def logout():
    response = logout_service()
    if response[1] == 200:
        flash(response[0].json['message'], "success_logout") 
        return redirect('/')
    

@customer.route('/account_profile', methods=['GET', 'POST'])
def account_profile():
    cust_id = session.get('cust_id')
    if not cust_id:
        return redirect('/')
    
    if request.method == 'POST':
        update_avatar_path(request.files)
        return redirect('/account_profile')
    total_quantity = CartService.get_total_quantity(cust_id)
    customer = getCustomer()
    if not customer:
        return redirect('/login')    
    return render_template('account_profile.html', customer=customer, total_quantity=total_quantity)
    
    
    

    
@customer.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    cust_id = session.get('cust_id')
    if not cust_id:
        return redirect('/')
    total_quantity = 0 
    customer = Customer.query.filter_by(id=session['cust_id']).first()
    total_quantity = Cart.query.filter_by(cust_id=session['cust_id']).with_entities(db.func.sum(Cart.quantity)).scalar() or 0
    if request.method == 'POST':
        success = update_customer_profile(request.form, request.files)
        return redirect('/account_profile')
    return render_template('update_profile.html', customer=getCustomer(), total_quantity=total_quantity)
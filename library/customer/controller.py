from flask import Blueprint, render_template, request, redirect, session, flash
from .service import signup as signup_service,login as login_service, logout as logout_service, update_customer_profile, getCustomer,update_avatar_path
from library.model import Customer
customer = Blueprint("customer", __name__)

@customer.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response = signup_service(request.form)  

        if response[1] == 200:  
            flash(response[0].json['message'], "success_signup")
            return redirect('/login')
        
        elif response[1] == 400:
            flash(response[0].json['message'], "error_signup")
            return redirect('/signup')

        flash(response[0].json['message'], "error")
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
    if request.method == 'POST':
        update_avatar_path(request.files)
        return redirect('/account_profile')
    customer = getCustomer()
    if not customer:
        return redirect('/login')    
    return render_template('account_profile.html', customer=customer)
    
    
    

    
@customer.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        success = update_customer_profile(request.form, request.files)
        return redirect('/account_profile')
    return render_template('update_profile.html', customer=getCustomer())
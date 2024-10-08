from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from .service import signup as signup_service, login as login_service, logout as logout_service

customer = Blueprint("customer", __name__)

@customer.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response = signup_service(request.form)  

        if response[1] == 200:  
            flash(response[0].json['message'], "success_signup")
            return redirect(url_for('customer.login'))
        
        elif response[1] == 400:
            flash(response[0].json['message'], "error_signup")
            return redirect(url_for('customer.signup'))

        flash(response[0].json['message'], "error")
        return redirect(url_for('customer.signup'))

    return render_template('signup.html')


@customer.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = login_service(request.form)  

        if response[1] == 200:  
            return redirect(url_for('main_page'))  

        flash(response[0].json['message'], "error")  
        return redirect(url_for('customer.login'))

    return render_template('login.html')


@customer.route('/logout')
def logout():
    response = logout_service()
    if response[1] == 200:
        flash(response[0].json['message'], "success_logout") 
        return redirect(url_for('main_page'))
    

@customer.route('/accout_profile')
def accout_profile():
    if 'cust_name' in session:
        return render_template('accout_profile.html', cust_name=session['cust_name'])
    else:
        return redirect(url_for('auth.login'))
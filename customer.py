from flask import Blueprint, render_template, redirect, session, url_for

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customer_info')
def customer_info():
    if 'cust_name' in session:
        return render_template('customer_info.html', cust_name=session['cust_name'])
    else:
        return redirect(url_for('auth.login'))
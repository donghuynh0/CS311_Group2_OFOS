from flask import render_template, session, redirect, url_for
from . import customer

@customer.route('/customer_info')
def customer_info():
    # Display the user's information or redirect to login if not available
    if 'cust_name' in session:
        return render_template('customer_info.html', cust_name=session['cust_name'])
    else:
        return redirect(url_for('auth.login'))
from flask import render_template, request, redirect, session, url_for, flash
from db import get_db
from . import auth

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        connection = get_db()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Customers WHERE Cust_Mail = %s"
                cursor.execute(sql, (email,))
                existing_user = cursor.fetchone()
                
                if not name and not email and not phone_number:
                    flash("Please enter your information.", "error")
                    return redirect(url_for('auth.signup'))

                if existing_user:
                    flash("Email already registered.", "error")
                    return redirect(url_for('auth.signup'))

                sql = "INSERT INTO Customers (Cust_Name, Cust_Mail, Contact_Number) VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, email, phone_number))
                connection.commit()

                flash("Account created successfully", "success")
                return redirect(url_for('auth.login'))

        finally:
            connection.close()

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        phone_number = request.form['phone_number']  
        
        connection = get_db()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Customers WHERE Cust_Mail = %s AND Contact_Number = %s"
                cursor.execute(sql, (email, phone_number))
                user = cursor.fetchone()

                if user:
                    session['cust_name'] = user['Cust_Name']  # Store username in session
                    return redirect(url_for('main_page'))
                else:
                    flash("Invalid email or phone number!", "error")
                    return redirect(url_for('auth.login'))
        finally:
            connection.close()

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_page'))
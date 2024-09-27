from flask import Flask, request, redirect, session, url_for, flash, render_template
from flask_cors import CORS
import pymysql 
import os

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            database='CS311_OFOS',
            user='root',
            passwd='Bemo1806@',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(f"Error connecting to the database: {e}")
    return conn


@app.route('/', methods=['GET'])
def main_page():
    cust_name = session.get('cust_name', None)
    return render_template('main_page.html', cust_name=cust_name)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']


        connection = db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Customers WHERE Cust_Mail = %s"
                cursor.execute(sql, (email,))
                existing_user = cursor.fetchone()
                
                if not name and not email and not phone_number:
                    flash("Please enter your information.", "error")
                    return redirect(url_for('signup'))

                if existing_user:
                    flash("Email already registered.", "error")
                    return redirect(url_for('signup'))

                sql = "INSERT INTO Customers (Cust_Name, Cust_Mail, Contact_Number) VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, email, phone_number))
                connection.commit()

                flash("Account created successfully", "success")
                return redirect(url_for('login'))

        finally:
            connection.close()

    return render_template('signup.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method =='POST':
        email = request.form['email']
        password = request.form['phone_number']  
        connection = db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Customers WHERE Cust_Mail = %s AND Contact_Number = %s"
                cursor.execute(sql, (email, password))
                user = cursor.fetchone()

                if user:
                    session['cust_name'] = user['Cust_Name']  # Store username in session
                    return redirect(url_for('main_page'))
                else:
                    flash("Invalid email or password!", "error")
                    return redirect(url_for('login'))
        finally:
            connection.close()
            
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_page'))

@app.route('/customer_info')
def customer_info():
    # Display the user's information or redirect to login if not available
    if 'cust_name' in session:
        return render_template('customer_info.html', cust_name=session['cust_name'])
    else:
        return redirect(url_for('login'))




if __name__ == "__main__":
    app.run(port=8000, debug=True)

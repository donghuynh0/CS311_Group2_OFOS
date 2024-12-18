from library.extension import db
from library.model import Customer
from flask import jsonify, session
import time
import os
from datetime import datetime, timedelta


def signup(form_data):
    cust_name = form_data.get('cust_name')
    contact_number = form_data.get('contact_number')
    email = form_data.get('email')
    password = form_data.get('password')
    
    new_customer = Customer(
        cust_name=cust_name,
        contact_number=contact_number,
        email=email,
        password=password 
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Sign up successfully!"}), 200



def login(form_data):
    email = form_data.get('email')
    password = form_data.get('password')

    customer = Customer.query.filter_by(email=email).first()

    if customer and customer.password == password:  
        session['cust_id'] = customer.id
        session['login_time'] = datetime.now().isoformat()
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
    
    
    
def check_session_timeout():
    if 'login_time' in session:
        login_time = datetime.fromisoformat(session['login_time'])
        expiration_time = login_time + timedelta(minutes=120)  # Set timeout period in minute
        if datetime.now() > expiration_time:
            session.pop('cust_id', None)
            session.pop('login_time', None)
    return None


def logout():
    session.clear()  
    return jsonify({"message": "Logged out successfully!"}), 200

def getCustomer():
    cust_id = session.get('cust_id')  
    customer = Customer.query.get(cust_id) 
    return customer
 
def update_avatar_path(files_data):
    cust_id = session.get('cust_id')
    customer = Customer.query.get(cust_id)
    uploads_dir = os.path.join('static', 'uploads')  
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    image_file = files_data.get('profile_image')
    image_path = None
    image_filename = None  

    if image_file:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'avif'}
        file_extension = image_file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise ValueError("Unsupported file type.")
        
        image_filename = f"{image_file.filename}"
        image_path = os.path.join(uploads_dir, image_filename)  
        print(image_path)
        file_exists = os.path.exists(f"library/static/uploads/{image_filename}")
        if not file_exists:
            image_file.save(f"library/static/uploads/{image_filename}")
    if image_filename:  
        customer.avatar_path = f"uploads/{image_filename}"
    db.session.commit()
 
def update_customer_profile(form_data, files_data):
    cust_id = session.get('cust_id') 
    
    try:        
        customer = Customer.query.get(cust_id)
        if customer:
            customer.cust_name = form_data.get('fullName')
            customer.contact_number = form_data.get('phoneNumber')
            customer.email = form_data.get('email')
            customer.gender = form_data.get('gender')
            customer.address = form_data.get('address')

            db.session.commit()
            return True
        else:
            print(f"No customer found with ID: {cust_id}")
            return False
    except Exception as e:
        print(f"Error updating customer profile: {e}")  
        db.session.rollback()
        return False
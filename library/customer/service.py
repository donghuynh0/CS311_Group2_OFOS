from library.extension import db
from library.model import Customer
from flask import jsonify, session

def signup(form_data):
    cust_name = form_data.get('cust_name')
    contact_number = form_data.get('contact_number')
    email = form_data.get('email')

    if cust_name and contact_number and email:
        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            return jsonify({"message": "Email is already registered. Please use a different email."}), 400
        try:
            new_customer = Customer(cust_name=cust_name, contact_number=contact_number, email=email)
            db.session.add(new_customer)
            db.session.commit()
            return jsonify({"message": "Sign up successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot sign up!"}), 400
    else:
        return jsonify({"message": "Invalid email or phone number"}), 400

def login(form_data):
    email = form_data.get('email')
    contact_number = form_data.get('contact_number')

    customer = Customer.query.filter_by(email=email).first()

    if customer and customer.contact_number == contact_number:  
        session['cust_name'] = customer.cust_name
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid email or phone number"}), 401

def logout():
    session.clear()  
    return jsonify({"message": "Logged out successfully!"}), 200
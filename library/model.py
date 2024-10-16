from .extension import db

from .extension import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    avatar_path = db.Column(db.String(255), nullable=True)  

    def __init__(self, cust_name, contact_number, email, address=None, gender=None, avatar_path=None):
        self.cust_name = cust_name
        self.contact_number = contact_number
        self.email = email
        self.address = address
        self.gender = gender
        self.avatar_path = avatar_path  


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rest_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15))
    address = db.Column(db.String(255))
    logo_image_path = db.Column(db.String(255)) 

    def __init__(self, rest_name, contact_number, address, logo_image_path=None):
        self.rest_name = rest_name
        self.contact_number = contact_number
        self.address = address
        self.logo_image_path = logo_image_path

class DeliveryPerson(db.Model):
    __tablename__ = 'deliverypersons'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deli_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15))
    email = db.Column(db.String(100))

    def __init__(self, deli_name, contact_number, email):
        self.deli_name = deli_name
        self.contact_number = contact_number
        self.email = email


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey('deliverypersons.id'), nullable=False)
    order_date = db.Column(db.Date, default=datetime.utcnow)
    order_address = db.Column(db.String(255))

    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
    restaurant = db.relationship('Restaurant', backref=db.backref('orders', lazy=True))
    delivery_person = db.relationship('DeliveryPerson', backref=db.backref('orders', lazy=True))

    def __init__(self, customer_id, restaurant_id, delivery_person_id, order_address):
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.delivery_person_id = delivery_person_id
        self.order_address = order_address


class OrderItem(db.Model):
    __tablename__ = 'orderitems'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    item_price = db.Column(db.Numeric(10, 2))

    order = db.relationship('Order', backref=db.backref('items', lazy=True))

    def __init__(self, order_id, item_name, item_price):
        self.order_id = order_id
        self.item_name = item_name
        self.item_price = item_price


class Payment(db.Model):
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    amount_payed = db.Column(db.Numeric(10, 2), nullable=False)
    amount_returned = db.Column(db.Numeric(10, 2))

    order = db.relationship('Order', backref=db.backref('payment', lazy=True))

    def __init__(self, order_id, total_amount, amount_payed, amount_returned):
        self.order_id = order_id
        self.total_amount = total_amount
        self.amount_payed = amount_payed
        self.amount_returned = amount_returned
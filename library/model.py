from .extension import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    avatar_path = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)  # Store plain-text password

    def __init__(self, cust_name, contact_number, email, password, address=None, gender=None, avatar_path=None):
        self.cust_name = cust_name
        self.contact_number = contact_number
        self.email = email
        self.address = address
        self.gender = gender
        self.avatar_path = avatar_path
        self.password = password 

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
    avatar_path = db.Column(db.String(255), nullable=True)  

    def __init__(self, deli_name, contact_number, email, avatar_path=None):
        self.deli_name = deli_name
        self.contact_number = contact_number
        self.email = email
        self.avatar_path = avatar_path

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey('deliverypersons.id'), nullable=True)  # Nullable to allow flexibility
    order_date = db.Column(db.Date, default=datetime.utcnow)
    order_address = db.Column(db.String(255))

    # Define the relationship with OrderItem
    order_items = db.relationship('OrderItem', back_populates='order', lazy=True)

    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
    restaurant = db.relationship('Restaurant', backref=db.backref('orders', lazy=True))
    delivery_person = db.relationship('DeliveryPerson', backref=db.backref('orders', lazy=True))

    def __init__(self, customer_id, restaurant_id, delivery_person_id=None, order_date=None, order_address=None):
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.delivery_person_id = delivery_person_id
        self.order_date = order_date or datetime.utcnow()
        self.order_address = order_address


class OrderItem(db.Model):
    __tablename__ = 'orderitems'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('restaurant_items.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    item_price = db.Column(db.Numeric(10, 2))
    quantity = db.Column(db.Integer, nullable=False)

    # Define the relationship back to Order
    order = db.relationship('Order', back_populates='order_items')
    restaurant_item = db.relationship('RestaurantItem', backref=db.backref('order_items', lazy=True))

    def __init__(self, order_id, item_id, item_name, item_price, quantity):
        self.order_id = order_id
        self.item_id = item_id
        self.item_name = item_name
        self.item_price = item_price
        self.quantity = quantity


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

class RestaurantItem(db.Model):
    __tablename__ = 'restaurant_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    item_price = db.Column(db.Numeric(10, 2), nullable=False)
    logo = db.Column(db.String(255), nullable=True)  

    restaurant = db.relationship('Restaurant', backref=db.backref('items', lazy=True))

    def __init__(self, restaurant_id, item_name, item_price, logo=None):
        self.restaurant_id = restaurant_id
        self.item_name = item_name
        self.item_price = item_price
        self.logo = logo
        
class Cart(db.Model):
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('restaurant_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    item = db.relationship('RestaurantItem', backref=db.backref('carts', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('cart_items', lazy=True))

    def __init__(self, cust_id, item_id, quantity=1):
        self.cust_id = cust_id  
        self.item_id = item_id
        self.quantity = quantity

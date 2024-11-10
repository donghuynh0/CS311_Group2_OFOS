from flask import Flask
from .extension import db, ma
import os
from .customer.cust_controller import customer
from .restaurants.rest_controller import restaurants
from .shopping.shop_controller import shop

def create_db(app):
    if not os.path.exists('library/library.db'):
        with app.app_context():
            db.create_all() 
            
            
def create_app(config_file = 'config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    ma.init_app(app)
    create_db(app)
    app.register_blueprint(restaurants) 
    app.register_blueprint(customer)  
    app.register_blueprint(shop) 
    return app



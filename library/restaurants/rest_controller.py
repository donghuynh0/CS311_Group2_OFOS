from flask import Blueprint, render_template, session, redirect
from .rest_service import get_all_restaurants, fetch_restaurant_items 
from library.shopping.shop_service import CartService
from library.model import Customer
restaurants = Blueprint('restaurants', __name__)

@restaurants.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    return get_all_restaurants()

@restaurants.route('/api/restaurant_items/<int:restaurant_id>', methods=['GET'])
def get_restaurant_items_route(restaurant_id): 
    return fetch_restaurant_items(restaurant_id)

@restaurants.route('/restaurant/<int:restaurant_id>')
def restaurant_page(restaurant_id):
    cust_id = session.get('cust_id')
    if not cust_id:
        return redirect('/')
    
    total_quantity = CartService.get_total_quantity(cust_id)
    customer = Customer.query.filter_by(id=cust_id).first() if cust_id else None
    return render_template('restaurant.html', restaurant_id=restaurant_id, total_quantity=total_quantity, customer=customer)


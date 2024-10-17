from flask import Blueprint
from .service import get_all_restaurants

restaurants = Blueprint('restaurants', __name__)

@restaurants.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    return get_all_restaurants()
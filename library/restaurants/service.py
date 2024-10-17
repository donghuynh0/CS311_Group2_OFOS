from library.model import Restaurant
from flask import jsonify

def get_all_restaurants():
    try:
        restaurants = Restaurant.query.all()
        
        restaurants_list = [{
            'title': restaurant.rest_name,
            'description': restaurant.address,
            'img': restaurant.logo_image_path
        } for restaurant in restaurants]
        
        return jsonify(restaurants_list)
    
    except Exception as e:
        return jsonify({"message": "Error fetching restaurants"}), 500

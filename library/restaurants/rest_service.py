from library.model import Restaurant, RestaurantItem
from flask import jsonify, url_for

def get_all_restaurants():
    try:
        restaurants = Restaurant.query.all()
        
        if not restaurants:
            print("No restaurants found in the database.")  # Log if the database is empty

        restaurants_list = [{
            'id': restaurant.id,
            'title': restaurant.rest_name,
            'description': restaurant.address,
            'img': restaurant.logo_image_path
        } for restaurant in restaurants]
        
        return jsonify(restaurants_list)
    
    except Exception as e:
        print(f"Error fetching restaurants: {e}")  # Log the exact error
        return jsonify({"message": "Error fetching restaurants"}), 500



def fetch_restaurant_items(restaurant_id):  
    items = RestaurantItem.query.filter_by(restaurant_id=restaurant_id).all()
    
    item_list = [{
        "id": item.id,
        "restaurant_id": item.restaurant_id,
        "item_name": item.item_name,
        "item_price": str(item.item_price),
        "logo": url_for('static', filename=item.logo.lstrip("static/")) if item.logo else url_for('static', filename='images/default-image.webp')
    } for item in items]
        
    return jsonify(item_list)

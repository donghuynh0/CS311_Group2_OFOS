from flask import Blueprint, jsonify, request, session, render_template
from .shop_service import CartService
from library.model import Cart, RestaurantItem, Customer, Order, OrderItem
from library.customer.cust_service import getCustomer
from library.extension import db

cart = Blueprint('cart', __name__)

@cart.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    cust_id = session.get('cust_id')  

    if not cust_id:
        return jsonify({'error': 'User not logged in'}), 401

    CartService.add_to_cart(cust_id, item_id, quantity)
    return jsonify({'message': 'Item added to cart'}), 200

@cart.route('/api/cart', methods=['GET'])
def get_cart():
    cust_id = session.get('cust_id')
    if not cust_id:
        return jsonify({'error': 'User not logged in'}), 401

    cart_items = CartService.get_cart_items(cust_id)
    return jsonify([{
        'item_id': item.item_id,
        'quantity': item.quantity,
    } for item in cart_items])
    
    
@cart.route('/api/cart/update_quantity', methods=['POST'])
def update_quantity():
    cust_id = session.get('cust_id')
    item_id = request.json.get('item_id')
    quantity = request.json.get('quantity')
    print("Received data:", {"cust_id": cust_id, "item_id": item_id, "quantity": quantity})  # Debug line

    cart_item = Cart.query.filter_by(cust_id=cust_id, item_id=item_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()

        subtotal = cart_item.quantity * cart_item.item.item_price
        total = sum(item.quantity * item.item.item_price for item in Cart.query.filter_by(cust_id=cust_id).all())

        return jsonify({'subtotal': subtotal, 'total': total}), 200
    else:
        return jsonify({'error': 'Item not found in cart'}), 404
   
    
    
    
@cart.route('/cart')
def cart_page():
    cust_id = session.get('cust_id')  
    cart_items = Cart.query.filter_by(cust_id=cust_id).join(RestaurantItem, Cart.item_id == RestaurantItem.id).all()

    customer = getCustomer()
    
    items = [
        {
            'id': item.id,
            'item_name': item.item.item_name,
            'price': float(item.item.item_price),
            'quantity': item.quantity,
            'subtotal': float(item.item.item_price) * item.quantity,
            'image_url': item.item.logo 
        }
        for item in cart_items
    ]

    return render_template('Shopping_cart.html', items=items, customer = customer)


@cart.route('/place_order')
def place_order():
    cust_id = session.get('cust_id')
    if not cust_id:
        return "User not logged in", 401

    customer = Customer.query.get(cust_id)
    
    cart_items = Cart.query.filter_by(cust_id=cust_id).join(RestaurantItem, Cart.item_id == RestaurantItem.id).all()

    items = [
        {
            'id': item.id,
            'item_name': item.item.item_name,
            'price': float(item.item.item_price),
            'quantity': item.quantity,
            'subtotal': float(item.item.item_price) * item.quantity,
            'image_url': item.item.logo 
        }
        for item in cart_items
    ]
    
    total_price = sum(item['subtotal'] for item in items)

    return render_template('place_order.html', customer=customer, items=items, total_price=total_price)


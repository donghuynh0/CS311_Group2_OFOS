from flask import Blueprint, jsonify, request, session, render_template, redirect
from .shop_service import CartService
from library.model import Cart, RestaurantItem, Customer, Order, OrderItem, DeliveryPerson
from library.customer.cust_service import getCustomer
from library.extension import db
from functools import wraps
import random
from sqlalchemy.sql.expression import func

shop = Blueprint('shop', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cust_id = session.get('cust_id')
        if not cust_id:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@shop.route('/api/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.json
    item_id = data.get('item_id')
    quantity = data.get('quantity')

    if not item_id or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({'error': 'Invalid item or quantity'}), 400

    cust_id = session.get('cust_id')
    CartService.add_to_cart(cust_id, item_id, quantity)
    return jsonify({'message': 'Item added to shop'}), 200

@shop.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    cust_id = session.get('cust_id')
    cart_items = CartService.get_cart_items(cust_id)
    formatted_items = format_cart_items(cart_items)
    return jsonify(formatted_items)

@shop.route('/api/cart/update_quantity', methods=['POST'])
@login_required
def update_quantity():
    cust_id = session.get('cust_id')
    item_id = request.json.get('item_id')
    quantity = request.json.get('quantity')

    if not item_id or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({'error': 'Invalid item or quantity'}), 400

    cart_item = Cart.query.filter_by(cust_id=cust_id, item_id=item_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()

        subtotal = cart_item.quantity * cart_item.item.item_price
        total = sum(item.quantity * item.item.item_price for item in Cart.query.filter_by(cust_id=cust_id).all())

        return jsonify({'subtotal': subtotal, 'total': total}), 200
    else:
        return jsonify({'error': 'Item not found in shop'}), 404

@shop.route('/api/cart/store_selected_items', methods=['POST'])
@login_required
def store_selected_items():
    data = request.get_json()
    selected_item_ids = data.get('items', [])
    
    # Store selected item IDs in the session
    session['selected_item_ids'] = selected_item_ids

    # Return a success response
    return jsonify({"success": True}), 200



@shop.route('/api/cart/place_order', methods=['POST'])
@login_required
def place_selected_order():
    cust_id = session.get('cust_id')
    selected_item_ids = session.get('selected_item_ids', [])
    if not selected_item_ids:
        return jsonify({"error": "No items selected"}), 400
    
    # Fetch the customer from the database to get the address
    customer = Customer.query.filter_by(id=cust_id).first()
    if not customer or not customer.address:
        return jsonify({"error": "Customer address not found"}), 400

    # Step 1: Get cart items for the selected item IDs
    cart_items = Cart.query.filter(Cart.cust_id == cust_id, Cart.item_id.in_(selected_item_ids)).all()
    if not cart_items:
        return jsonify({"error": "No items found in the cart"}), 400

    # Step 2: Group items by restaurant_id
    items_by_restaurant = {}
    for item in cart_items:
        restaurant_id = item.item.restaurant_id
        if restaurant_id not in items_by_restaurant:
            items_by_restaurant[restaurant_id] = []
        items_by_restaurant[restaurant_id].append(item)

    order_ids = []  # Store new order IDs for this transaction

    # Step 3: Create separate orders for each restaurant
    for restaurant_id, items in items_by_restaurant.items():
        delivery_person = DeliveryPerson.query.order_by(func.rand()).first()
        if not delivery_person:
            return jsonify({"error": "No delivery person available"}), 400

        # Create a new order for this restaurant
        new_order = Order(
            customer_id=cust_id,
            restaurant_id=restaurant_id,
            delivery_person_id=delivery_person.id,
            order_address= customer.address  
        )
        db.session.add(new_order)
        db.session.flush()  # To get the new order ID immediately

        # Add each item as an OrderItem for this order
        for cart_item in items:
            order_item = OrderItem(
                order_id=new_order.id,
                item_id=cart_item.item_id,
                item_name=cart_item.item.item_name,
                item_price=cart_item.item.item_price,
                quantity=cart_item.quantity
            )
            db.session.add(order_item)

        db.session.commit()  # Commit the order and items for this restaurant

        order_ids.append(new_order.id)  # Store the order ID for this transaction

    # Step 4: Remove selected items from the cart after placing the order
    Cart.query.filter(Cart.cust_id == cust_id, Cart.item_id.in_(selected_item_ids)).delete(synchronize_session=False)
    db.session.commit()

    # Append new order IDs to the session order_ids list
    if 'order_ids' not in session:
        session['order_ids'] = []
    session['order_ids'].extend(order_ids)  # Append new order IDs

    # Clear selected items from the session
    session.pop('selected_item_ids', None)

    return jsonify({"success": True, "order_ids": order_ids}), 200



@shop.route('/cart')
@login_required
def cart_page():
    cust_id = session.get('cust_id')
    cart_items = Cart.query.filter_by(cust_id=cust_id).join(RestaurantItem, Cart.item_id == RestaurantItem.id).all()
    customer = getCustomer()
    
    items = format_cart_items(cart_items)
    return render_template('Shopping_cart.html', items=items, customer=customer)

@shop.route('/place_order')
@login_required
def place_order_page():
    cust_id = session.get('cust_id')
    selected_item_ids = session.get('selected_item_ids', [])

    if not selected_item_ids:
        return redirect('/cart')  # Redirect back to cart if no items are selected

    # Fetch only the selected items from the cart
    cart_items = (
        Cart.query
        .filter(Cart.cust_id == cust_id, Cart.item_id.in_(selected_item_ids))
        .join(RestaurantItem, Cart.item_id == RestaurantItem.id)
        .all()
    )

    # Prepare items for display
    items = [
        {
            'item_name': cart_item.item.item_name,
            'price': float(cart_item.item.item_price),
            'quantity': cart_item.quantity,
            'subtotal': float(cart_item.item.item_price) * cart_item.quantity,
            'image_url': cart_item.item.logo
        }
        for cart_item in cart_items
    ]

    # Calculate the total price
    total_price = sum(item['subtotal'] for item in items)

    # Fetch customer information
    customer = getCustomer()

    # Render the template with items and total price
    return render_template('place_order.html', customer=customer, items=items, total_price=total_price)




@shop.route('/order_details')
@login_required
def order_details():
    order_ids = session.get('order_ids')
    if not order_ids:
        return redirect('/cart')  # Redirect if no order ID is found

    # Fetch all orders based on the order_ids stored in session
    orders = Order.query.filter(Order.id.in_(order_ids)).all()
    if not orders:
        return redirect('/cart')  # Redirect if no matching orders are found

    # Assume the same customer for all orders (if this assumption holds true)
    customer = orders[0].customer

    # Prepare order details for each order
    order_details_list = []
    for order in orders:
        delivery_person = order.delivery_person

        # Use the relationship `order_items` directly
        items = [
            {
                'item_name': item.item_name,
                'item_price': item.item_price,
                'quantity': item.quantity,
                'subtotal': item.item_price * item.quantity,
                'image_url': item.restaurant_item.logo
            } 
            for item in order.order_items
        ]
        print(items)

        total_price = sum(item['subtotal'] for item in items)

        # Append details for each order
        order_details_list.append({
            'order_id': order.id,
            'delivery_person': delivery_person,
            'order_items': items,
            'total_price': total_price
        })

    return render_template('order_details.html', orders=order_details_list, customer=customer)






# Helper function to format shop items for consistency
def format_cart_items(cart_items):
    return [
        {
            'id': item.item_id,
            'item_name': item.item.item_name,
            'price': float(item.item.item_price),
            'quantity': item.quantity,
            'subtotal': float(item.item.item_price) * item.quantity,
            'image_url': item.item.logo
        }
        for item in cart_items
    ]

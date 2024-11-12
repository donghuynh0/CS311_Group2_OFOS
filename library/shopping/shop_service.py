from library.model import Cart
from library.extension import db

class CartService:
    @staticmethod
    def add_to_cart(cust_id, item_id, quantity):
        existing_cart_item = Cart.query.filter_by(cust_id=cust_id, item_id=item_id).first()
        print(item_id)
        if existing_cart_item:
            existing_cart_item.quantity += quantity
        else:
            new_cart_item = Cart(cust_id=cust_id, item_id=item_id, quantity=quantity)
            db.session.add(new_cart_item)
        db.session.commit()

    @staticmethod
    def get_cart_items(cust_id):
        return Cart.query.filter_by(cust_id=cust_id).all()
    
    def get_total_quantity(cust_id):
        total_quantity = db.session.query(db.func.sum(Cart.quantity)).filter_by(cust_id=cust_id).scalar()
        return total_quantity or 0 

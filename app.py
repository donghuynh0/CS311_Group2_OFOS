from library import create_app
from flask import session, render_template
from library.model import Customer, Cart
from library.extension import db
from library.restaurants.rest_service import get_all_restaurants

app = create_app()

@app.route('/')
def main_page():
    customer = None
    total_quantity = 0  

    if 'cust_id' in session:
        customer = Customer.query.filter_by(id=session['cust_id']).first()
        total_quantity = Cart.query.filter_by(cust_id=session['cust_id']).with_entities(db.func.sum(Cart.quantity)).scalar() or 0

    return render_template('main_page.html', customer=customer, total_quantity=total_quantity)


@app.template_filter('currency')
def currency(value):
    """Format a number as currency."""
    return "${:,.2f}".format(value)

if __name__ == "__main__":
    app.run(debug=True, port=8080)

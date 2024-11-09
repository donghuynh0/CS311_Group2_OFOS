from library import create_app
from flask import session, render_template
from library.model import Customer
from library.restaurants.rest_service import get_all_restaurants

app = create_app()

@app.route('/')
def main_page():
    if 'cust_id' in session:
        customer = Customer.query.filter_by(id=session['cust_id']).first()
    else:
        customer = None
    
    return render_template('main_page.html', customer=customer)

@app.template_filter('currency')
def currency(value):
    """Format a number as currency."""
    return "${:,.2f}".format(value)

if __name__ == "__main__":
    app.run(debug=True, port=8080)

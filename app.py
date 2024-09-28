from flask import Flask, session, render_template
from flask_cors import CORS
import os
from db import init_app
from auth import auth
from customer import customer 

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

init_app(app)

# register blueprints
app.register_blueprint(auth)
app.register_blueprint(customer)


@app.route('/')
def main_page():
    cust_name = session.get('cust_name', None)
    return render_template('main_page.html', cust_name=cust_name)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
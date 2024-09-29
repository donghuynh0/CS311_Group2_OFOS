from library import create_app
from flask import session, render_template

app = create_app()


@app.route('/')
def main_page():
    cust_name = session.get('cust_name', None)
    return render_template('main_page.html', cust_name=cust_name)


if __name__ == "__main__":
    app.run(debug=True)
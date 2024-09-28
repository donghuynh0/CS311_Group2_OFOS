import pymysql
from flask import  g

def get_db():
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            database='CS311_OFOS',
            user='root',
            passwd='Bemo1806@',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(f"Error connecting to the MySQL database: {e}")
        conn = None
    return conn

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
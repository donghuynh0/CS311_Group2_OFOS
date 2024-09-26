from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymysql 

app = Flask(__name__)
CORS(app)

def db_connection():
    conn = None
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
        print(f"Error connecting to the database: {e}")
    return conn





if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)

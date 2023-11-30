from flask import Flask
from flask import render_template   
from flask import request
from flask import redirect

from flask import jsonify
from flask_cors import CORS
import json
import psycopg2

app = Flask(__name__)
CORS(app)

# PostgreSQL Instance configurations
app.config['DB_USER'] = 'BUILDER'
app.config['DB_PASSWORD'] = 'cls2'
app.config['DB_NAME'] = 'postgres'
app.config['DB_HOST'] = 'localhost'
app.config['DB_PORT'] = '54321'

def get_db_connection():
    return psycopg2.connect(
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME'],
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT']
    )

@app.route("/add", methods=['POST'])
def add():
    data = request.get_json()
    name = data.get('Name')
    email = data.get('Email')  # Corrected variable name

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('''INSERT INTO cc_student(Name, Email) VALUES (%s, %s)''', (name, email))
        connection.commit()

        return jsonify({"Result": "Success"})

    finally:
        cursor.close()
        connection.close()

@app.route("/", methods=['GET'])
def render_students():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('''SELECT * FROM cc_student''')
        rv = cursor.fetchall()

        results = []
        for row in rv:
            result = {
                'Name': row[0],
                'Email': row[1],
                'ID': row[2]
            }
            results.append(result)

        response = {'results': results, 'count': len(results)}
        return render_template('index.html', **response)

    finally:
        cursor.close()
        connection.close()
        
@app.route("/delete", methods=['POST'])
def delete_by_id():
    delete_id = request.form.get('DeleteID')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('''DELETE FROM cc_student WHERE ID = %s''', (delete_id,))
        connection.commit()

        return redirect('/')

    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

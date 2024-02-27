from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login_index():
    if request.method == 'POST':
        # sqlite
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        # html form 
        name = request.form['name']
        password = request.form['password']

        query = "SELECT name,password FROM users where name= '"+name+"' and password='"+password+"'"
        cursor.execute(query)
        results = cursor.fetchall()

        if len(results) == 0:
            print("Invalid Crediantials")
        else:
            print("br")
            return render_template('home_index.html')
        # print(name, password)

    return render_template('login_index.html')
    

@app.route('/')
def home_index():
    return render_template('home_index.html')

@app.route('/date_lookup')
def date_lookup():
    return render_template('date_lookup_index.html')

@app.route('/my_reservations')
def my_reservations():
    return render_template('my_reservations_index.html')

@app.route('/reservation_history')
def reservation_history():
    return render_template('reservation_history_index.html')

# @app.route('/bug_report')
# def bug_report():
#     return render_template('bug_report.html')


if __name__ == '__main__':
    app.run(debug=True)
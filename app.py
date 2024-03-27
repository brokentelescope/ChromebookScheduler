from flask import Flask, request, render_template, jsonify
from datetime import datetime
import sqlite3, os, sys, json
current_dir = os.path.dirname(os.path.abspath(__file__))
python_files_dir = os.path.join(current_dir, 'chromebook_util')
sys.path.append(python_files_dir)
import create_chromebook
import check_chromebook
import edit_chromebook
import all_available

app = Flask(__name__)

@app.route('/edit_chromebook', methods=['POST'])
def edit_chromebooks():
    data = request.json
    print(data)
    date = data['date']
    period = data['period']
    id = data['id']
    name = data['name']
    edit_chromebook.edit(id, date, period, name)

    # code to update reservation history
    with open('reservation_history.txt', 'a') as file:
        file.write(", ".join([date, period, id, name]) + '\n')
        print('helo')
        
    return jsonify('Success')

@app.route('/check', methods=['POST'])
def check():
    data = request.json 
    date = data['date']
    period = data['period']
    id = data['id']
    return jsonify(check_chromebook.check(id, date, period))

@app.route('/check_chromebooks', methods=['POST'])
def check_chromebooks():
    data = request.json
    date = data['date']
    period = data['period']
    available = all_available.available_chromebooks(date, period)
    return jsonify(available)

@app.route('/create-chromebook-file', methods=['POST'])
def create_chromebook_file():
    data = request.json 
    location = data['location']
    admin = data['admin']
    amt = data['amt']
    id = data['id']

    if admin != '1':
        return jsonify('Invalid Admin Password')
    create_chromebook.create(id, 2024, location, amt)
    return jsonify('Success')

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
            print("Invalid Credentials")
        else:
            print("Valid Credentials")
            json_data = {'my_variable': name}  # Create JSON data
            with open('data.json', 'w') as json_file:
                json.dump(json_data, json_file)
            return render_template('home_index.html')
        # print(name, password)

    return render_template('login_index.html')
    
@app.route('/get_data')
def get_data():
    # Load the data from data.json
    with open('data.json', 'r') as file:
        data = json.load(file)  # Use json.load to parse JSON data
    # Return the JSON data
    return jsonify(data)  # Use jsonify to return JSON response

@app.route('/home_index')
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

@app.route('/add_locations')
def add_locations():
    return render_template('add_locations.html')

# @app.route('/bug_report')
# def bug_report():
#     return render_template('bug_report.html')


if __name__ == '__main__':
    app.run(debug=True)
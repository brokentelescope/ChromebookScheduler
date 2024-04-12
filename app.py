from flask import *
from datetime import datetime
import sqlite3, os, sys, json
current_dir = os.path.dirname(os.path.abspath(__file__))
python_files_dir = os.path.join(current_dir, 'chromebook_util')
sys.path.append(python_files_dir)
import create_chromebook
import check_chromebook
import edit_chromebook
import all_available
import cancel_chromebook

app = Flask(__name__)
app.secret_key = 'key'

username = ''

@app.route('/get_reserved', methods = ['POST'])
def get_reserved():
    global username
    reservedByUser = []
    # here we have to go read all the file, and all the line, make a check to see if name is ok, and append it

    folder_name = 'chromebook_data'
    # for id in os.listdir(folder_name): #A2, A32, etc 
    cnt = 0
    reservedByUser = []
    for id in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, id)):
            print(os.path.join(folder_name, id))
            with open(os.path.join(folder_name, id), 'r') as file:
                for line in file:
                    if username in line:
                        ID = all_available.get_info(id)[0]
                        loc = all_available.get_info(id)[1]   
                        reservedByUser.append([ID, loc, line.split(',')[0], line.split(',')[1],line.split(',')[2]] )
    return jsonify(reservedByUser)


@app.route('/cancel_chromebook', methods=['POST'])
def cancel_chromebooks(): 
    global username
    data = request.json
    date = data['date']
    period = data['period']
    id = data['id']  
    print(date, period, id)
    cancel_chromebook.cancel(id, date, period)
 
    return jsonify('Success')
@app.route('/edit_chromebook', methods=['POST'])
def edit_chromebooks():
    global username
    data = request.json
    date = data['date']
    period = data['period']
    id = data['id']
    name = username
    edit_chromebook.edit(id, date, period, name)

    # code to update reservation history
    with open('reservation_history.txt', 'a') as file:
        file.write(",".join([date, period, id, name]) + '\n')
        
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

@app.route('/get_history', methods = ['POST'])
def get_history():
    available = []
    with open('reservation_history.txt', 'r') as file:
        for line in file:
            available.append(line.strip().split(','))
    return jsonify(sorted(available)) 

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
    global username
    # clear any previous flash messages
    flash('')
    if request.method == 'POST':
        data = request.form
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        # SIGN UP 
        if len(data) == 3:
            name = request.form['name']
            password = request.form['password']

            query = "SELECT name FROM users where name='"+name+"'"
            cursor.execute(query)
            results = cursor.fetchall()
            # username already exists
            if len(results):
                flash("Username already exists. Please choose a different one.")
                return render_template('login_index.html')
            else:
                cursor.execute(f"INSERT INTO users VALUES ('{name}', '{password}')")
                connection.commit()
                flash("Sign up successful. You can now login.")
                return render_template('login_index.html')

        else:
            name = request.form['name']
            password = request.form['password']

            query = "SELECT name,password FROM users where name= '"+name+"' and password='"+password+"'"
            cursor.execute(query)
            results = cursor.fetchall()

            if len(results) == 0:
                flash("Invalid Credentials. Please try again.")
            else:
                print("Valid Credentials")
                username = name
                print(username)
                return render_template('home_index.html')

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
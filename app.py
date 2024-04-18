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

@app.route('/check_bin', methods=['POST'])
def check_bin():
    bin_id = request.form['binId']
    is_duplicate = 0
    folder_name = 'chromebook_data' 
    for id in os.listdir(folder_name):
        if id == bin_id: is_duplicate = 1
    
    return jsonify({'is_duplicate': is_duplicate})

@app.route('/verify_account', methods=['POST'])
def verify_account():  
    data = request.json
    userName = data['userName']
    updated_lines = []

    with open('user_data.txt', 'r') as file:
        for line in file: 
            line = line.strip()
            if userName in line:
                # Split the line and change the last value to 1
                parts = line.split(',')
                parts[-1] = '1'
                line = ','.join(parts)
            updated_lines.append(line)

    # Write back the updated lines to the file
    with open('user_data.txt', 'w') as file:
        for line in updated_lines:
            file.write(line + '\n')

    return jsonify('Success')

@app.route('/remove_account', methods=['POST'])
def remove_account(): 
    global username
    data = request.json
    userName = data['userName']
    with open('user_data.txt', 'r') as file:
        lines_to_keep = [line.strip() for line in file if userName not in line]

    with open('user_data.txt', 'w') as file:
        for line in lines_to_keep:
            file.write(line + '\n')

    return jsonify('Success')


@app.route('/get_account', methods = ['POST'])
def get_account(): 
    reservedByUser = []  

    with open('user_data.txt', 'r') as file:
        for line in file: 
            reservedByUser.append([line.split(',')[0],line.split(',')[2]] )
    return jsonify(reservedByUser)

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
            # print(os.path.join(folder_name, id))
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
    # print(date, period, id)
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
                # Redirect to home_index.html after successful login
                return redirect(url_for('home_index'))

    return render_template('login_index.html')
    
@app.route('/get_data')
def get_data():
    # Load the data from data.json
    with open('data.json', 'r') as file:
        data = json.load(file)  # Use json.load to parse JSON data
    # Return the JSON data
    return jsonify(data)  # Use jsonify to return JSON response

def checkAdmin():
    global username 
    is_admin = (username == 'ADMIN') 
    return is_admin

@app.route('/home_index')
def home_index():
    # Call the checkAdmin function to determine if the user is an admin
    is_admin = checkAdmin() 
    return render_template('home_index.html', is_admin=is_admin)

@app.route('/date_lookup')
def date_lookup():
    is_admin = checkAdmin() 
    return render_template('date_lookup_index.html', is_admin=is_admin) 

@app.route('/my_reservations')
def my_reservations():
    is_admin = checkAdmin() 
    return render_template('my_reservations_index.html', is_admin=is_admin)  

@app.route('/reservation_history')
def reservation_history():
    is_admin = checkAdmin() 
    return render_template('reservation_history_index.html', is_admin=is_admin)   

@app.route('/add_locations')
def add_locations():
    is_admin = checkAdmin() 
    return render_template('add_locations.html', is_admin=is_admin)   

@app.route('/team')
def team():
    is_admin = checkAdmin() 
    return render_template('team.html', is_admin=is_admin)

@app.route('/admin_panel')
def admin_panel():
    is_admin = checkAdmin() 
    return render_template('admin_panel.html', is_admin=is_admin)    

# @app.route('/bug_report')
# def bug_report():
#     return render_template('bug_report.html')

if __name__ == '__main__':
    app.run(debug=True)
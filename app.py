
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
import database_util
import get_info

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
    username = data['userName']
    # Connect to the database
    result = database_util.get_single_data(username)
    print(result)
    if result:
        is_verified = bool(result[2])
        # Toggle verification status
        new_verification = 1 if not is_verified else 0
        database_util.verify(username, new_verification)
        if not is_verified:
            return jsonify('The account has been verified.')
        return jsonify('The account has been unverified.')
    else:
        return jsonify('The account is not found.')  

@app.route('/remove_account', methods=['POST'])
def remove_account(): 
    data = request.json
    database_util.remove(data['userName'])
    return jsonify('Success')

# @app.route('/check_chromebooks', methods=['POST'])
# def check_chromebooks():
#     global username
#     data = request.json
#     chromebooks_data = all_available.available_chromebooks(data['date'], data['period'])
#     is_verified = checkVerify()

#     response_data = {
#         "chromebooks": chromebooks_data,
#         "is_verified": is_verified
#     }
#     return jsonify(response_data)


@app.route('/get_account', methods = ['POST'])
def get_account(): 
    is_verified = checkVerify()

    response_data = {
        "data": database_util.get_all_data(),
        "is_verified": is_verified
    }
    return jsonify(response_data) 

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
                        ID = get_info.get_info(id)[0]
                        loc = get_info.get_info(id)[1]   
                        reservedByUser.append([ID, loc, line.split(',')[0], line.split(',')[1],line.split(',')[2]] )
    return jsonify(reservedByUser)

@app.route('/get_current_locations', methods = ['POST'])
def get_current_locations():   
    data = request.json
    date = data['date']
    period = data['period']
    print(date, period)
    f = 'chromebook_data' 
    a = []
    for id in os.listdir(f):    
        if os.path.isfile(os.path.join(f, id)): 
            with open(os.path.join(f, id), 'r') as file:
                for line in file:
                    if date+','+period in line:
                        if "none" not in line: 
                            bin = id
                            source = get_info.get_info(id)[1]      
                            classroom = line.split(',')[3] 
                            by = line.split(',')[2]
                            a.append([bin, source, classroom, by])
                        else: 
                            bin = id
                            source = get_info.get_info(id)[1]      
                            a.append([bin, source, source, "N/A"])
                            

    return jsonify(a)

# @app.route('/get_unreserved_locations', methods = ['POST'])
# def get_current_locations(): 


@app.route('/', methods=['GET', 'POST'])
def login_index():
    global username
    # clear any previous flash messages
    flash('')
    if request.method == 'POST':
        data = request.form 
        # SIGN UP 
        if len(data) == 4:
            name = data['name']
            password = data['password'] 
            classroom = data['classroom']

            query = database_util.get_single_data(name)
            # username already exists
            if query:
                flash("Username already exists. Please choose a different one.")
            else:
                database_util.insert_user(name, password, classroom)
                flash("Sign up successful. You can now login.")
            return render_template('login_index.html')

        else:
            name = data['name']
            password = data['password']
            connection = sqlite3.connect('user_data.db')
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM users WHERE username=?", (name,))
            result = cursor.fetchone() 
            print(result, password)
            if result and result[0] == password:
                print("Valid Credentials")
                username = name
                return redirect(url_for('home_index'))  
            else:
                flash("Invalid Credentials. Please try again.")

                
    return render_template('login_index.html') 
 
@app.route('/cancel_chromebook', methods=['POST'])
def cancel_chromebooks(): 
    global username
    data = request.json
    date = data['date']
    period = data['period']
    id = data['id']  
    edit_chromebook.edit(id, date, period, 'none', 'none')
    return jsonify('Success')


@app.route('/edit_chromebook', methods=['POST'])
def edit_chromebooks():
    global username
    data = request.json
    date = data['date']
    period = data['period']
    id = data['id']
    name = username
    using_custom_classroom = data['using_custom_classroom']

    if (using_custom_classroom == 0): 
        print(191)
        classroom = database_util.get_classroom(username)  
    else: 
        classroom = using_custom_classroom 
    

    print(classroom)
    edit_chromebook.edit(id, date, period, name, classroom) 
    with open('reservation_history.txt', 'a') as file:
        file.write(",".join([date, period, id, name]) + '\n') # can include to where if needed
        
    return jsonify('Success')

@app.route('/check', methods=['POST'])
def check():
    data = request.json 
    return jsonify(check_chromebook.check(data['id'], data['date'], data['period']))

def checkVerify():
    global username 
    # Connect to the database
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT isVerified FROM users WHERE username=?", (username,)) 
    result = cursor.fetchone()
    if result:
        is_verified = bool(result[0])  
        connection.close()
        return is_verified
    else:
        connection.close()
        return False  
    
@app.route('/check_chromebooks', methods=['POST'])
def check_chromebooks():
    global username
    data = request.json
    chromebooks_data = all_available.available_chromebooks(data['date'], data['period'])
    is_verified = checkVerify()

    response_data = {
        "chromebooks": chromebooks_data,
        "is_verified": is_verified
    }
    return jsonify(response_data)

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
    amt = data['amt']
    id = data['id']
    print(data, location, amt, id)
    create_chromebook.create(id, 2024, location, amt)
    return jsonify('Success')
 
    
@app.route('/get_data')
def get_data(): 
    with open('data.json', 'r') as file:
        data = json.load(file)   
    return jsonify(data)   

def checkAdmin():
    global username 
    is_admin = (username == 'ADMIN') 
    return is_admin

@app.route('/current_locations')
def current_locations():
    is_admin = checkAdmin() 
    is_verified = checkVerify()  
    return render_template('current_locations.html', is_admin=is_admin, is_verified=is_verified)  

@app.route('/home_index')
def home_index(): 
    is_admin = checkAdmin() 
    is_verified = checkVerify() 
    return render_template('home_index.html', is_admin=is_admin, is_verified=is_verified)

@app.route('/date_lookup')
def date_lookup():
    is_admin = checkAdmin()  
    is_verified = checkVerify() 
    return render_template('date_lookup_index.html', is_admin=is_admin, is_verified=is_verified)

@app.route('/my_reservations')
def my_reservations():
    is_admin = checkAdmin() 
    is_verified = checkVerify() 
    return render_template('my_reservations_index.html', is_admin=is_admin, is_verified=is_verified) 

@app.route('/reservation_history')
def reservation_history():
    is_admin = checkAdmin() 
    is_verified = checkVerify()
    return render_template('reservation_history_index.html', is_admin=is_admin, is_verified=is_verified)   

@app.route('/add_locations')
def add_locations():
    is_admin = checkAdmin() 
    is_verified = checkVerify()     
    return render_template('add_locations.html', is_admin=is_admin, is_verified=is_verified)      

@app.route('/team')
def team():
    is_admin = checkAdmin() 
    is_verified = checkVerify()     
    return render_template('team.html', is_admin=is_admin, is_verified=is_verified)      

@app.route('/admin_panel')
def admin_panel():
    is_admin = checkAdmin() 
    is_verified = checkVerify()  
    return render_template('admin_panel.html', is_admin=is_admin, is_verified=is_verified)     

# @app.route('/bug_report')
# def bug_report():
#     return render_template('bug_report.html')

if __name__ == '__main__':
    app.run(debug=True)



 
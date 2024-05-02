
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
import get_info
import database_util

app = Flask(__name__)
app.secret_key = 'key'

username = ''  

@app.route('/check_bin', methods=['POST'])
def check_bin():
    bin_id = request.form['binId']
    is_duplicate = 0
    folder_name = 'chromebook_data' 
    # Check each file name in the chromebook_data folder
    for id in os.listdir(folder_name):
        if id == bin_id: 
            is_duplicate = 1
            break
    return jsonify({'is_duplicate': is_duplicate}) 
    
@app.route('/verify_account', methods=['POST'])
def verify_account():
    data = request.json
    username = data['userName']
    result = database_util.get_single_data(username)
    if result:
        # Data is in the form of (username, password, isVerified), so take result[2]
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

# ?
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
    reservedByUser = []
    for id in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, id)):
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
                            by = line.split(',')[2]
                            a.append([bin, source, by])
                        else: 
                            bin = id
                            source = get_info.get_info(id)[1]      
                            a.append([bin, source, "N/A"])
                            

    return jsonify(a)


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
            query = database_util.get_single_data(name)
            # username already exists
            if query:
                flash("Username already exists. Please choose a different one.")
            else:
                database_util.insert_user(name, password)
                flash("Sign up successful. You can now login.")
            return render_template('login_index.html')

        else:
            name = data['name']
            password = data['password']
            result = database_util.get_single_data(name)
            if result and result[1] == password:
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
    edit_chromebook.edit(id, date, period, 'none')
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
    with open('reservation_history.txt', 'a') as file:
        file.write(",".join([date, period, id, name]) + '\n') # can include to where if needed
        
    return jsonify('Success')

@app.route('/check', methods=['POST'])
def check():
    data = request.json 
    return jsonify(check_chromebook.check(data['id'], data['date'], data['period']))
    
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
    year = datetime.now().year
    create_chromebook.create(id, year, location, amt)
    return jsonify('Success')

@app.route('/get_data')
def get_data(): 
    with open('data.json', 'r') as file:
        data = json.load(file)   
    return jsonify(data)   

"""
Function that checks if the user is the admin.
Input:
    This function uses the global variable: username (string) as input. 
Returns:
    (bool)
"""
def checkAdmin():
    global username 
    return username == 'ADMIN'
"""
Function that checks if the user is verifed.
Input:
    This function uses the global variable: username (string) as input. 
Returns:
    (bool)
"""
def checkVerify():
    global username 
    result = database_util.get_single_data(username)
    if result:
        is_verified = bool(result[2])  
        return is_verified
    return False  

"""
The below functions are flask routes that render the html templates in our templates folder.
The functions have three additional parameters in the render_template function.
    active_page: which page they are actively viewing. this is used to highlight the active page.
    is_admin: whether the user is an admin or not. this determines whether they can access the admin-only pages.
    is_verified: whether the user is verifided or not. this determines whether they can reserve chromebooks or not.
Args:
    none
Returns:
    (render_template)
"""
@app.route('/current_locations')
def current_locations():
    return render_template('current_locations_index.html', active_page='current_locations', is_admin=checkAdmin(), is_verified=checkVerify())  

@app.route('/home_index')
def home_index(): 
    return render_template('home_index.html', active_page='home_index', is_admin=checkAdmin(), is_verified=checkVerify())

@app.route('/date_lookup')
def date_lookup():
    return render_template('date_lookup_index.html', active_page='date_lookup', is_admin=checkAdmin(), is_verified=checkVerify())

@app.route('/my_reservations')
def my_reservations():
    return render_template('my_reservations_index.html', active_page='my_reservations', is_admin=checkAdmin(), is_verified=checkVerify()) 

@app.route('/reservation_history')
def reservation_history():
    return render_template('reservation_history_index.html', active_page='reservation_history', is_admin=checkAdmin(), is_verified=checkVerify())   

@app.route('/add_locations')
def add_locations():    
    return render_template('add_locations_index.html', active_page='add_locations', is_admin=checkAdmin(), is_verified=checkVerify())      

@app.route('/team')
def team():    
    return render_template('team_index.html', active_page='team', is_admin=checkAdmin(), is_verified=checkVerify())      

@app.route('/admin_panel')
def admin_panel(): 
    return render_template('admin_panel_index.html', active_page='admin_panel', is_admin=checkAdmin(), is_verified=checkVerify())

if __name__ == '__main__':
    app.run(debug=True)



 
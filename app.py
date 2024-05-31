"""
Flask App File
ICS4U-04
Owen, Steven, Rex
File containing all the Flask routes and functions that make our project work.
History:
Feb 21, 2024: Program creation
"""
from flask import *
from datetime import datetime
import os, sys, json
current_dir = os.path.dirname(os.path.abspath(__file__))
python_files_dir = os.path.join(current_dir, 'chromebook_util')
sys.path.append(python_files_dir)
import create_chromebook
import check_chromebook
import edit_chromebook
import all_available 
import get_info
import database_util
import update_availability
import datetime

app = Flask(__name__)
app.secret_key = 'key'

username = ''   

@app.route('/get_date_range', methods=['GET'])
def get_date_range():
    file_path = os.path.join('data', 'dateMaintained.txt')
    try:
        with open(file_path, 'r') as file:
            start_date = file.readline().strip()
            end_date = file.readline().strip()
        return jsonify(start=start_date, end=end_date)
    except Exception as e:
        return jsonify(error=str(e)), 500
    
@app.route('/get_day')
def get_day():
    month_names_to_numbers = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    
    month_name = request.args.get('month')
    day = int(request.args.get('day'))
    cnt = 0
    # Convert month name to number
    month_number = month_names_to_numbers.get(month_name)
    
    # Read the contents of the text file
    with open('INPUTGOOGLESHEET.txt', 'r') as file:
        lines = file.readlines() 
        # Iterate through each line to find the matching entry
        for line in lines:  
            cnt += 1
            parts = line.strip().split(',')
            if cnt > 10:
                entry_month = int(parts[0])
                entry_day = int(parts[1])
                value = parts[2]
                # print(entry_month, month_number, entry_day, day)
                if entry_month == month_number and entry_day == day:
                    if value == "1" or value == "2" or value == "3" or value == "4":
                        value = "Day " + value 
                    if value == "H":
                        value = "Holiday"
                    if value == "PD":
                        value = "PD Day"
                    # Matching entry found, return the value
                    return jsonify({
                        'schoolDay': value,
                        'className': 'school-day'  # Adjust class name as needed
                    }) 
        return jsonify({
            'schoolDay': "No Data",
            'className': 'school-day'  # Adjust class name as needed
        })  

@app.route('/updateYear', methods=['POST'])
def updateYear():  
    # Update the date range
    file_path = 'data/dateMaintained.txt'
    with open(file_path, 'r') as file:
        start_date = file.readline().strip()
        end_date = file.readline().strip()
    
    # Convert the dates to datetime objects
    start_date_obj = datetime.datetime.strptime(start_date, "%Y,%m,%d")
    end_date_obj = datetime.datetime.strptime(end_date, "%Y,%m,%d")
    
    # Calculate the first day of the next month for start_date
    next_month_start = (start_date_obj.month % 12) + 1
    next_year_start = start_date_obj.year + ((start_date_obj.month - 1) // 12)
    new_start_date_obj = datetime.datetime(next_year_start, next_month_start, 1)
    
    # Calculate the first day of the next month for end_date
    next_month_end = (end_date_obj.month % 12) + 1
    next_year_end = end_date_obj.year + ((end_date_obj.month - 1) // 12)
    new_end_date_obj = datetime.datetime(next_year_end, next_month_end, 1)
    
    # Calculate the number of days shifted
    days_shifted = (new_start_date_obj - start_date_obj).days
    
    # Write the new dates back to the file
    with open(file_path, 'w') as file:
        file.write(new_start_date_obj.strftime("%Y,%m,%d") + '\n')
        file.write(new_end_date_obj.strftime("%Y,%m,%d") + '\n')
    
    # Execute the availability update script
    # Assuming update_availability is imported correctly
    for i in range(days_shifted): 
        update_availability.execute()
    
    # Print the number of days shifted
    print(days_shifted)
    
    return jsonify(message='Update availability script executed successfully')



@app.route('/check_bin', methods=['POST'])
def check_bin():
    bin_id = request.form['binId']
    is_duplicate = 0
    folder_name = os.path.join('data', 'chromebook_data')
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
@app.route('/get_bins', methods = ['POST'])
def get_bins():  
    response_data = {
        "data": database_util.get_all_data(), 
    }
    return jsonify(response_data) 

@app.route('/get_account', methods = ['POST'])
def get_account(): 
    is_verified = checkVerify()
    response_data = {
        "data": database_util.get_all_data(),
        "is_verified": is_verified
    }
    return jsonify(response_data) 

@app.route('/get_reserved', methods=['POST'])
def get_reserved():  
    global username
    reservedByUser = []
    # Define the path to the chromebook_data folder within the data directory
    folder_name = os.path.join('data', 'chromebook_data')
    
    # Iterate over each file in the chromebook_data folder
    for id in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, id)):
            with open(os.path.join(folder_name, id), 'r') as file:
                for line in file:
                    if username in line:
                        ID = get_info.get_info(id)[0]
                        loc = get_info.get_info(id)[1]
                        reservedByUser.append([ID, loc, line.split(',')[0], line.split(',')[1], line.split(',')[2]])

    # Sort reservedByUser by date in descending order
    reservedByUser = sorted(reservedByUser, key=lambda x: x[2], reverse=True)

    print(reservedByUser)
    return jsonify(reservedByUser)


@app.route('/get_current_locations', methods=['POST'])
def get_current_locations():   
    data = request.json
    date = data['date']
    period = data['period']
    folder_name = os.path.join('data', 'chromebook_data')
    a = []
    
    for id in os.listdir(folder_name):    
        if os.path.isfile(os.path.join(folder_name, id)): 
            with open(os.path.join(folder_name, id), 'r') as file:
                for line in file:
                    if date + ',' + period in line:
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
        if len(data) == 3:
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

        # SIGN IN
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

@app.route('/delete_chromebook', methods=['POST'])
def delete_chromebook(): 
    data = request.json 
    id = data['id'] 

    # Directory where the text files are stored
    folder_name = os.path.join('data', 'chromebook_data')

    # File path of the text file to be deleted
    file_path = os.path.join(folder_name, id)

    # Check if the file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        return jsonify('Success')
    else:
        return jsonify('File not found'), 404
@app.route('/edit_chromebook', methods=['POST'])
def edit_chromebooks():
    global username
    data = request.json
    date = data['date']
    period = data['period']
    id = data['id']
    name = username 

    edit_chromebook.edit(id, date, period, name) 
    with open(os.path.join('data', 'reservation_history.txt'), 'a') as file:  # Changed 'w' to 'a'
        file.write(",".join([date, period, id, name]) + '\n')
        
    return jsonify('Success') 

@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        # Path to the reservation history file
        file_path = os.path.join('data', 'reservation_history.txt')

        # Clear the contents of the file
        open(file_path, 'w').close()
        
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error clearing reservation history: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/check', methods=['POST'])
def check():
    data = request.json 
    return jsonify(check_chromebook.check(data['id'], data['date'], data['period']))
    
@app.route('/get_chromebooks', methods=['POST'])
def get_chromebooks():  
    a = []
    folder_name = os.path.join('data', 'chromebook_data')

    for id in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, id)): 
            a.append(get_info.get_info(id)) 
             
    response_data = {
        "chromebooks": a 
    }
    return jsonify(response_data)


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
    with open(os.path.join('data', 'reservation_history.txt'), 'r') as file:


        for line in file:
            available.append(line.strip().split(','))
    return jsonify(sorted(available)) 

@app.route('/create-chromebook-file', methods=['POST'])
def create_chromebook_file():
    data = request.json 
    location = data['location'] 
    amt = data['amt']
    id = data['id'] 
    create_chromebook.create(id, location, amt)
    return jsonify('Success')

@app.route('/get_data')
def get_data(): 
    with open(os.path.join('data', 'reservation_history.txt'), 'r') as file:
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



 
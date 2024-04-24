"""
Database utility functions
ICS4U-03
Owen, Rex, Steven 
We decided to include all database util functions in the same file rather
than have them in separate files since the functions are pretty short.
"""

import sqlite3
connection = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = connection.cursor()

"""
Function that creates the database with keys: username, password, isVerified
Args:
    none
Returns:
    none
"""
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            isVerified INTEGER
        )
    ''')
    connection.commit()

# create_table()

"""
Function that returns the data associated with a username, to check if sign-in credentials are valid.
Args:
    username: (string)
Returns:
    (tuple) 
    Tuple in format of (username, password, verified)
"""
def get_single_data(username):
    cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    return cursor.fetchone()

"""
Function that returns all a list of all usernames and passwords to display in Admin Panel.
Args:
    none
Returns:
    (list of tuples)
    Tuples in a format of (username, verified)
"""
def get_all_data():
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    for i in range(len(data)):
        # omit the passwords since we do not need to display them
        data[i] = (data[i][0], data[i][2])
    return data

"""
Function that inserts a new user into the database.
Args:
    username (string)
    password (string)
    classroom (string)
    isVerified (int)
Returns:
    none
"""
def insert_user(username, password, classroom, isVerified=0):
    cursor.execute("INSERT INTO users (username, password, isVerified, classroom) VALUES (?, ?, ?, ?)", (username, password, isVerified, classroom))
    connection.commit()

"""
Function that changes the verification status of a user.
Args:
    username (string)
    isVerified (int)
Returns:
    none
"""
def verify(username, isVerified):
    cursor.execute("UPDATE users SET isVerified=? WHERE username=?", (isVerified, username))
    connection.commit()

"""
Function that removes a user from the database.
Args:
    username (string)
Returns:
    none
"""
def remove(username):
    cursor.execute(f"DELETE FROM users WHERE username='{username}'")
    connection.commit()

"""
Function that gets the classroom of a user from the database.
Args:
    classroom (string)
Returns:
    none
"""
def get_classroom(username):    
    cursor.execute(f"SELECT classroom FROM users WHERE username='{username}'")

    result = cursor.fetchone()
    print(result)
    # print(username, result)

    return result[0] 
 
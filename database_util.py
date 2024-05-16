"""
Database utility functions
ICS4U-03
Owen, Rex, Steven 
We decided to include all database util functions in the same file rather
than have them in separate files since the functions are pretty short.
History:
Apr 18, 2024: Program creation
"""
import sqlite3

def create_table():
    """
    Function that creates the database with keys: username, password, isVerified
    Args:
        none
    Returns:
        none
    """
    # These two lines need to be copied into each function separately.
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            isVerified INTEGER
        )
    ''')
    connection.commit()

# create_table()

def get_single_data(username):
    """
    Function that returns the data associated with a username, to check if sign-in credentials are valid.
    Args:
        username: (string)
    Returns:
        (tuple) 
        Tuple in format of (username, password, verified)
    """
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    return cursor.fetchone()

def get_all_data():
    """
    Function that returns all a list of all usernames and passwords to display in Admin Panel.
    Args:
        none
    Returns:
        (list of tuples)
        Tuples in a format of (username, verified)
    """
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    for i in range(len(data)):
        # omit the passwords since we do not need to display them
        data[i] = (data[i][0], data[i][2])
    return data

def insert_user(username, password, isVerified=0):
    """
    Function that inserts a new user into the database.
    Args:
        username (string)
        password (string) 
        isVerified (int)
    Returns:
        none
    """
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password, isVerified) VALUES (?, ?, ?)", (username, password, isVerified))
    connection.commit()

def verify(username, isVerified):
    """
    Function that changes the verification status of a user.
    Args:
        username (string)
        isVerified (int)
    Returns:
        none
    """
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET isVerified=? WHERE username=?", (isVerified, username))
    connection.commit()
# verify('ADMIN', 1)

def remove(username):
    """
    Function that removes a user from the database.
    Args:
        username (string)
    Returns:
        none
    """
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM users WHERE username='{username}'")
    connection.commit()

def get_classroom(username):    
    """
    Function that gets the classroom of a user from the database.
    Args:
        classroom (string)
    Returns:
        none
    """
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT classroom FROM users WHERE username='{username}'")

    result = cursor.fetchone()
    # print(result)
    # print(username, result)

    return result[0] 
 
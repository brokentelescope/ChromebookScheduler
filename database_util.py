import sqlite3

connection = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = connection.cursor()

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

def get_single_data(username):
    cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    return cursor.fetchone()

def get_all_data():
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    for i in range(len(data)):
        # omit the passwords
        data[i] = (data[i][0], data[i][2])
    return data

def insert_user(username, password, isVerified=0):
    cursor.execute("INSERT INTO users (username, password, isVerified) VALUES (?, ?, ?)", (username, password, isVerified))
    connection.commit()

def verify(username):
    cursor.execute("UPDATE users SET isVerified=? WHERE username=?", (1, username))
    connection.commit()

def remove(username):
    cursor.execute(f"DELETE FROM users WHERE username='{username}'")
    connection.commit()

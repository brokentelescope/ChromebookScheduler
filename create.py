import sqlite3

connection = sqlite3.connect("user_data.db")

cursor = connection.cursor()

cursor.execute("INSERT INTO users VALUES ('ADMIN', '1234')")

connection.commit()

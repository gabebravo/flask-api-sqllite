import sqlite3

connection = sqlite3.connect('data.db')  # db file

cursor = connection.cursor()

# users + columns // id INTEGER PRIMARY KEY = syntax for auto-incrmenting
create_users_table = 'CREATE TABLE if NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_users_table)

create_items_table = 'CREATE TABLE if NOT EXISTS items (name text, price real)'
cursor.execute(create_items_table)

connection.commit()
connection.close()  # tells sql to close db connection

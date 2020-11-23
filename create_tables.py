import sqlite3

connection = sqlite3.connect('data.db')  # db file

cursor = connection.cursor()

# users + columns // id INTEGER PRIMARY KEY = syntax for auto-incrmenting
create_table = 'CREATE TABLE if NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_table)

connection.close()  # tells sql to close db connection


# # inserting multiple rows
# users = [
#     (2, 'willy', 'aaaa'),
#     (3, 'billy', 'bbbb'),
# ]
# cursor.executemany(insert_query, users)

# # get/show all rows in the db
# select_query = 'SELECT * FROM users'
# for row in cursor.execute(select_query):
#     print(row)

# connection.commit()  # tells sql to save to db

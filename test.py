import sqlite3

connection = sqlite3.connect('data.db')  # db file

cursor = connection.cursor()

# users + columns
create_table = 'CREATE TABLE users (id int, username text, password text)'
cursor.execute(create_table)

# inserting one row
user = (1, 'gabe', 'asdf')  # user record as tuple
# (?, ?, ?) syntax is for columns
insert_query = 'INSERT INTO users VALUES (?, ?, ?)'
cursor.execute(insert_query, user)

# inserting multiple rows
users = [
    (2, 'willy', 'aaaa'),
    (3, 'billy', 'bbbb'),
]
cursor.executemany(insert_query, users)

# get/show all rows in the db
select_query = 'SELECT * FROM users'
for row in cursor.execute(select_query):
    print(row)

connection.commit()  # tells sql to save to db

connection.close()  # tells sql to close db connection

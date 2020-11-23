from __future__ import annotations
from flask_restful import Resource, reqparse
import sqlite3
from dataclasses import dataclass
from typing import Union


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()  # parsed request payload
        connection = sqlite3.connect('data.db')  # db file
        cursor = connection.cursor()

        # NULL here in lieu of id
        insert_query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(insert_query, (data['username'], data['password']))

        connection.commit()  # tells sql to save to db
        connection.close()  # tells sql to close db connection

        return {"message": "User created successfully"}, 201


@dataclass
class User:
    id: int
    username: str
    password: str

    # print our string object
    def __repr__(self):
        return f'<User id:{self.id}, username:{self.username}, password:{self.password}>'

    # get user in sqlite by useranme
    @classmethod  # denotes class method, self/User references = cls
    def find_by_username(cls, username: str) -> Union[User, None]:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE username=?'  # ? syntax is for a param
        # this is the param as a tuple
        result = cursor.execute(query, (username,))
        row = result.fetchone()

        if row:
            user = cls(*row)  # spread operator
        else:
            user = None

        connection.close()
        return user

    # get user in sqlite by id
    @classmethod  # denotes class method, self/User references = cls
    def find_by_id(cls, _id: int) -> Union[User, None]:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE id=?'  # ? syntax is for a param
        # this is the param as a tuple
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)  # spread operator
        else:
            user = None

        connection.close()
        return user

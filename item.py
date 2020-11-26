import sqlite3
from sqlite3.dbapi2 import connect
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'  # ? syntax is for a param
        result = cursor.execute(query)  # this is the param as a tuple
        rows = result.fetchall()
        connection.close()

        if len(rows) > 0:
            return {'items': list(map(lambda row: {'name': row[0], 'price': row[1]}, rows))}, 200
        return {'message': 'There are no Items at this time'}, 400


class Item(Resource):
    # will only allow these keys to be parsed from the request payload
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @classmethod
    def find_by_name(cls, name: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'  # ? syntax is for a param
        result = cursor.execute(query, (name,))  # this is the param as a tuple
        row = result.fetchone()
        connection.close()

        return row

    @classmethod
    def insert_item(cls, name: str, price: float):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(insert_query, (name, price))
        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, name: str, price: float):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(insert_query, (price, name))
        connection.commit()
        connection.close()

    @jwt_required()  # decorator will do the auth check before accessing the GET
    def get(self, name: str):
        row = self.find_by_name(name)

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200
        return {'message': 'Item not found'}, 400

    def post(self):
        data = Item.parser.parse_args()  # parsed request payload
        row = self.find_by_name(data['name'])
        # convert data to a json obj
        item = {'name': data['name'], 'price': data['price']}

        if row:
            # 400: problem with request
            return {'message': f"An item with name {row[0]} already exists."}, 400

        try:
            self.insert_item(item['name'], item['price'])
        except:
            # 500: Internal server error - problem with server
            return {'message': 'An error occurred inserting item.'}, 500

        return {"item": item}, 201

    def delete(self, name: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        delete_query = 'DELETE FROM items WHERE name=?'
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()

        return {'message': f'Item {name} has been deleted'}, 201

    def put(self):
        data = Item.parser.parse_args()
        item = {'name': data['name'], 'price': data['price']}

        row = self.find_by_name(item['name'])

        if row is None:  # no match, so add it to the db
            try:
                self.insert_item(item['name'], item['price'])
            except:
                {'message': 'An error occured while trying to save the item'}, 500
        else:  # found a match by name, so just update price
            try:
                self.update_item(item['name'], item['price'])
            except:
                {'message': 'An error occured while trying to update the item'}, 500

        return item, 201

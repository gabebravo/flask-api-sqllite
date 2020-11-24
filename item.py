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
            return {'items': list(map(lambda row: {'item': {'name': row[0], 'price': row[1]}}, rows))}, 200
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
            return {'message': f"An item with name {row[0]} already exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(insert_query, (item['name'], item['price']))
        connection.commit()
        connection.close()

        return item, 201

    def delete(self):
        global items  # this is used for overwriting the global var with assignment below
        data = request.get_json()  # entire request payload, not parsed
        print(data)
        items = list(
            filter(lambda item: item['name'] != data['name'], items))

        return {'message': f"Items deleted"}, 200

    def put(self):
        data = Item.parser.parse_args()
        item = next(
            filter(lambda x: x['name'] == data['name'], items), None)

        if(item is None):
            items.append(data)
        else:
            item.update(data)  # can simply update the found item

        return data, 201

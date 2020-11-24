from security import authenticate, identity
from user import UserRegister
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'yowzers'  # in produciton make this an env var - DO NOT EXPOSE
api = Api(app)

jwt = JWT(app, authenticate, identity)  # this will forward to the /auth route
# first calls authenticate, gets JWT, and then forwards it to identity

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item', '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':  # runs app if the file that runs the app is the same
    # important to mention debug=True, defaults to port:5000
    app.run(debug=True)

from flask import Flask, jsonify
from flask_restful import Api
from resources.users import UserRegister, UserLogin, User, UserLogout
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from sql_alchemy import database
from config import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_db():
  database.create_all()

@jwt.token_in_blocklist_loader
def verify_blacklist(self, token):
  return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def access_token_invalid(jwt_header, jwt_payload):
  return jsonify({ "message": "you need to login first" }), 401

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(User, '/users/<string:id>')

if __name__ == '__main__':
  migrate = Migrate(app, database)
  database.init_app(app)
  app.run(host='0.0.0.0', debug=True)
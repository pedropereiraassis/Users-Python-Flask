from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from decouple import config
DATABASE_URL = config('DATABASE_URL')
JWT_SECRET_KEY = config('JWT_SECRET_KEY')

database = SQLAlchemy()
migrate = Migrate()

def create_app():

  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
  app.config['JWT_BLACKLIST_ENABLED'] = True
  app.config['']
  api = Api(app)
  jwt = JWTManager(app)

  @jwt.token_in_blocklist_loader
  def verify_blacklist(self, token):
    return token['jti'] in BLACKLIST

  @jwt.revoked_token_loader
  def access_token_invalid(jwt_header, jwt_payload):
    return jsonify({ "message": "you need to login first" }), 401

  database.init_app(app)
  migrate.init_app(app, database)

  from models import user
  from resources.users import UserRegister, UserLogin, User, UserLogout

  api.add_resource(UserRegister, '/register')
  api.add_resource(UserLogin, '/login')
  api.add_resource(UserLogout, '/logout')
  api.add_resource(User, '/users/<string:id>')

  return app
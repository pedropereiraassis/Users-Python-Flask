from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from decouple import config
from datetime import timedelta

database = SQLAlchemy()
migrate = Migrate()

def create_app():

  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL').replace("postgres://", "postgresql://")
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['PROPAGATE_EXCEPTIONS'] = True
  app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY')
  app.config['JWT_BLACKLIST_ENABLED'] = True
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
  app.config['SESSION_COOKIE_HTTPONLY'] = True
  app.config['REMEMBER_COOKIE_HTTPONLY'] = True
  app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
  api = Api(app)
  jwt = JWTManager(app)

  @jwt.token_in_blocklist_loader
  def verify_blacklist(self, token):
    return token['jti'] in BLACKLIST

  @jwt.revoked_token_loader
  def access_token_invalid(jwt_header, jwt_payload):
    return jsonify({ "message": "hello! you need to login first" }), 401

  database.init_app(app)
  migrate.init_app(app, database)

  from models import user
  from resources.users import UserRegister, UserLogin, User, UserLogout, Home, Users

  api.add_resource(UserRegister, '/register')
  api.add_resource(UserLogin, '/login')
  api.add_resource(UserLogout, '/logout')
  api.add_resource(User, '/users/<string:id>')
  api.add_resource(Users, '/users')
  api.add_resource(Home, '/')

  return app
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from blacklist import BLACKLIST
import re

email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

class UserRegister(Resource):

  @staticmethod
  def post():
    arguments = reqparse.RequestParser()
    arguments.add_argument('nome', type=str, required=True, help="field 'nome' cannot be null")
    arguments.add_argument('cpf', type=str, required=True, help="field 'cpf' cannot be null")
    arguments.add_argument('email', type=str, required=True, help="field 'email' cannot be null")
    arguments.add_argument('endereco', type=dict, required=True, help="field 'endereco' cannot be null")
    arguments.add_argument('pis', type=str, required=True, help="field 'pis' cannot be null")
    arguments.add_argument('admin', type=bool, default=False)
    arguments.add_argument('senha', type=str, required=True, help="field 'senha' cannot be null")
    arguments.add_argument('confirm_senha', type=str, required=True, help="field 'confirm_senha' cannot be null")
    data = arguments.parse_args()
        
    if not  re.search(email_regex,data['email']):
      return { "message": "invalid email" }, 400
    
    if not all(key in data['endereco'] for key in ( "nacionalidade", "estado", "municipio", "cep", "rua", "numero" )):
      return { "message": "field 'endereco' must be correctly fulfilled" }, 400

    if len(data['cpf']) != 11:
      return { "message": "invalid cpf, must have 11 digits" }, 400

    if len(data['pis']) != 11:
      return { "message": "invalid pis, must have 11 digits" }, 400

    if UserModel.find_by_cpf(data['cpf']):
      return { "message": f"cpf '{data['cpf']}' already registered" }, 400
    
    if data['senha'] != data['confirm_senha']:
      return { "message": "passwords doesn't match" }, 400

    user = UserModel(**data)
    try:
      user.set_password(senha=data['senha'])
      user.save_user()
      user = UserModel.find_by_cpf(data['cpf'])
      user.set_user_id(user)
    except:
      return { "message": "error while trying to save user" }, 500
    return { "message": "user registered successfully", "user": user.json() }, 201

class UserLogin(Resource):

  @staticmethod
  def post():
    arguments = reqparse.RequestParser()
    arguments.add_argument('cpf', type=str, required=True, help="field 'cpf' cannot be null")
    arguments.add_argument('senha', type=str, required=True, help="field 'senha' cannot be null")
    data = arguments.parse_args()

    if len(data['cpf']) != 11:
      return { "message": "invalid cpf, must have 11 digits" }, 400

    user = UserModel.find_by_cpf(data['cpf'])

    if user and user.check_password(senha=data['senha']):
      token = create_access_token(identity=user.id)
      return { "message": "user logged in successfully", "token": token }, 200
    
    return { "message": "invalid credentials" }, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
      jwt_id = get_jwt()['jti']
      BLACKLIST.add(jwt_id)
      return { "message": "user logged out successfully" }, 200

class Users(Resource):
  
  @jwt_required()
  def get(self):

    session_user_id = get_jwt_identity()
    session_user = UserModel.find_by_id(session_user_id)
    
    if not session_user:
      return { "message": "hello! you need to login first" }, 401

    if session_user.admin == True:
      try:
        users = UserModel.get_all_users()
        return { "users": [user.json() for user in users] }, 200
      except:
        return { "message": "error while trying to get users" }, 500
    return { "message": "oops, you can't do that" }, 403

class User(Resource):

  @jwt_required()
  def get(self, id):
    try:
      user = UserModel.find_by_id(id)
    except:
      return { "message": "invalid id" }, 400
    if user:
      return user.json()
    return { "message": "user not found" }, 404

  @jwt_required()
  def put(self, id):
    session_user_id = get_jwt_identity()
    session_user = UserModel.find_by_id(session_user_id)

    if not session_user:
      return { "message": "hello! you need to login first" }, 401
    
    try:
      user = UserModel.find_by_id(id)
    except:
      return { "message": "invalid id" }, 400

    if not user:
      return { "message": "user not found" }, 404

    if (session_user.admin == True) or (str(user.id) == str(session_user_id)):
      arguments = reqparse.RequestParser()
      arguments.add_argument('nome', type=str, required=True, help="field 'nome' cannot be null")
      arguments.add_argument('email', type=str, required=True, help="field 'email' cannot be null")
      arguments.add_argument('endereco', type=dict, required=True, help="field 'endereco' cannot be null")
      arguments.add_argument('pis', type=str, required=True, help="field 'pis' cannot be null")
      data = arguments.parse_args()

      if not  re.search(email_regex,data['email']):
        return { "message": "invalid email" }, 400
      
      if not all(key in data['endereco'] for key in ( "nacionalidade", "estado", "municipio", "cep", "rua", "numero" )):
        return { "message": "field 'endereco' must be correctly fulfilled" }, 400

      if len(data['pis']) != 11:
        return { "message": "invalid pis, must have 11 digits" }, 400

      try:
        user.update_user(**data)
        user.save_user()
      except:
        return { "message": "error while trying to update user"}, 500
      return { "message": "user updated successfully", "user": user.json() }, 200
    return { "message": "oops, you can't do that" }, 403
  
  @jwt_required()
  def delete(self, id):
    session_user_id = get_jwt_identity()
    session_user = UserModel.find_by_id(session_user_id)

    if not session_user:
      return { "message": "hello! you need to login first" }, 401
    
    try:
      user = UserModel.find_by_id(id)
    except:
      return { "message": "invalid id" }, 400

    if not user:
      return { "message": "user not found"}, 404
    
    if (session_user.admin == True) or (str(user.id) == str(session_user_id)):

      try:
        user.delete_user()
      except:
        return { "message": "error while trying to delete user"}, 500
      if str(user.id) == str(session_user_id):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return { "message": "you deleted your user so we logged you out" }, 200
      return { "message": "user deleted" }, 200
    return { "message": "oops, you can't do that" }, 403
    

class Home(Resource):

  @jwt_required()
  def get(self):
    session_user_id = get_jwt_identity()
    session_user = UserModel.find_by_id(session_user_id)

    if not session_user:
      return { "message": "hello! you need to login first" }, 401
    return{ "message": f"hello {session_user.nome}! Welcome to Users-Flask API." }, 200

from flask_restful import Resource, reqparse, request
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST

class UserRegister(Resource):

  @staticmethod
  def post():
    arguments = reqparse.RequestParser()
    arguments.add_argument('nome', type=str, required=True, help="Field 'nome' cannot be null")
    arguments.add_argument('cpf', type=str, required=True, help="Field 'cpf' cannot be null")
    arguments.add_argument('email', type=str, required=True, help="Field 'email' cannot be null")
    arguments.add_argument('endereco', type=dict, required=True, help="Field 'endereco' cannot be null")
    arguments.add_argument('pis', type=str, required=True, help="Field 'pis' cannot be null")
    arguments.add_argument('senha', type=str, required=True, help="Field 'senha' cannot be null")
    arguments.add_argument('confirm_senha', type=str, required=True, help="Field 'confirm_senha' cannot be null")
    data = arguments.parse_args()

    if UserModel.find_by_cpf(data['cpf']):
      print(UserModel.find_by_cpf(data['cpf']))
      return { "message": f"cpf '{data['cpf']}' already registered" }, 400
    
    if data['senha'] != data['confirm_senha']:
      return { "message": "passwords doesn't match" }, 400

    user = UserModel(**data)
    try:
      user.set_password(senha=data['senha'])
      user.save_user()
    except:
      return { "message": "error while trying to save user" }, 500
    return { "message": "user registered successfully", "user": user.json() }, 201

class UserLogin(Resource):

  @staticmethod
  def post():
    arguments = reqparse.RequestParser()
    arguments.add_argument('cpf', type=str, required=True, help="Field 'cpf' cannot be null")
    arguments.add_argument('senha', type=str, required=True, help="Field 'senha' cannot be null")
    data = arguments.parse_args()

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


class User(Resource):

  @jwt_required()
  def get(self, id):
    user = UserModel.find_by_id(id)
    if user:
      return user.json()
    return { "message": "user not found" }, 404

  @jwt_required()
  def put(self, id):
    arguments = reqparse.RequestParser()
    arguments.add_argument('nome', type=str, required=True, help="Field 'nome' cannot be null")
    arguments.add_argument('email', type=str, required=True, help="Field 'email' cannot be null")
    arguments.add_argument('endereco', type=dict, required=True, help="Field 'endereco' cannot be null")
    arguments.add_argument('pis', type=str, required=True, help="Field 'pis' cannot be null")
    data = arguments.parse_args()
    user = UserModel.find_by_id(id)
    if user:
      user.update_user(**data)
      try:
        user.save_user()
      except:
        return { "message": "error while trying to update user"}, 500
      return user.json(), 200
    return { "message": "user not found" }, 404
  
  @jwt_required()
  def delete(self, id):
    user = UserModel.find_by_id(id)
    if user:
      try:
        user.delete_user()
      except:
        return { "message": "error while trying to delete user"}, 500
      return { "message": "user deleted" }, 200
    return { "message": "user not found"}, 404
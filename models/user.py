from app import database
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID 
from datetime import datetime
from uuid import uuid4
class UserModel(database.Model):
  __tablename__ = 'users'
  id = database.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
  nome = database.Column(database.String(40), nullable=False)
  email = database.Column(database.String(40), nullable=False)
  endereco = database.Column(database.JSON, nullable=False)
  cpf = database.Column(database.String(11), nullable=False)
  pis = database.Column(database.String(40), nullable=False)
  senha = database.Column(database.String(), nullable=False)
  created_at = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

  def __init__(self, nome, email, endereco, cpf, pis, senha, confirm_senha):
    self.nome = nome
    self.email = email
    self.endereco = endereco
    self.cpf = cpf
    self.pis = pis
    self.senha = senha
    self.confirm_senha = confirm_senha
    self.id = None
  
  def set_password(self, senha):
    self.senha = generate_password_hash(senha)
  
  def check_password(self, senha):
    return check_password_hash(self.senha, senha)

  def json(self):
    return {
      'id': str(self.id),
      'nome': self.nome,
      'email': self.email,
      'endereco': self.endereco,
      'cpf': self.cpf,
      'pis': self.pis
    }
  
  @classmethod
  def find_by_id(cls, id):
    user = cls.query.filter_by(id=id).first()
    if user:
      return user
    return None
  
  @classmethod
  def find_by_cpf(cls, cpf):
    user = cls.query.filter_by(cpf=cpf).first()
    if user:
      return user
    return None
  
  def set_user_id(self, user):
    self.id = user.id

  def save_user(self):
    database.session.add(self)
    database.session.commit()
  
  def update_user(self, nome, email, endereco, pis):
    self.nome = nome
    self.email = email
    self.endereco = endereco
    self.pis = pis
  
  def delete_user(self):
    database.session.delete(self)
    database.session.commit()
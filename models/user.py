from sql_alchemy import database
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
  senha = database.Column(database.String(40), nullable=False)
  created_at = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

  def __init__(self, nome, email, endereco, cpf, pis, senha, confirm_senha):
    self.nome = nome
    self.email = email
    self.endereco = endereco
    self.cpf = cpf
    self.pis = pis
    self.senha = senha
    self.confirm_senha = confirm_senha
  
  def json(self):
    return {
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